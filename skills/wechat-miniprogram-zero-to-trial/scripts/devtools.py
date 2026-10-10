#!/usr/bin/env python3
"""Local inspection and explicit WeChat DevTools preview/upload. Python 3.9+."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def inspect_project(project):
    root = Path(project).expanduser().resolve()
    config = json.loads((root / 'project.config.json').read_text(encoding='utf-8'))
    if not isinstance(config, dict):
        raise ValueError('project.config.json 必须是对象')
    for field in ('appid', 'projectname'):
        if not isinstance(config.get(field), str) or not config[field].strip():
            raise ValueError(f'project.config.json 缺少有效 {field}')
    mini_root = config.get('miniprogramRoot', '.')
    if not isinstance(mini_root, str):
        raise ValueError('miniprogramRoot 必须是路径字符串')
    mini = (root / mini_root).resolve()
    if mini != root and root not in mini.parents:
        raise ValueError('miniprogramRoot 位于工程外，请先核对工程目录')
    for name in ('app.js', 'app.json'):
        if not (mini / name).is_file():
            raise ValueError(f'缺少 {mini / name}；框架项目请先构建为微信工程')
    app = json.loads((mini / 'app.json').read_text(encoding='utf-8'))
    if not isinstance(app, dict) or not isinstance(app.get('pages'), list) or not app['pages']:
        raise ValueError('app.json 缺少非空 pages 数组')
    return {
        'project': str(root), 'miniprogram_root': str(mini),
        'appid': config['appid'], 'projectname': config['projectname'],
        'first_page': app['pages'][0],
        'scope': '仅检查本地配置；未验证登录、页面编译、云端或体验版',
    }


def find_cli(explicit):
    candidates = [explicit] if explicit else [
        os.environ.get('WECHAT_DEVTOOLS_CLI'),
        '/Applications/wechatwebdevtools.app/Contents/MacOS/cli',
        str(Path.home() / 'Applications/wechatwebdevtools.app/Contents/MacOS/cli'),
        shutil.which('wechat-devtools-cli'),
    ]
    for candidate in candidates:
        if candidate:
            path = Path(candidate).expanduser().resolve()
            if path.is_file():
                if path.suffix.lower() in ('.bat', '.cmd'):
                    raise ValueError('Windows 批处理请按官方帮助直接调用 cli.bat；本脚本不通过 shell 执行命令')
                if os.access(path, os.X_OK):
                    return str(path)
    raise ValueError('找不到可执行的微信开发者工具 CLI，请用 --cli 指定实际文件路径')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inspect', 'preview', 'upload'))
    parser.add_argument('--project', required=True)
    parser.add_argument('--cli', help='可直接执行的开发者工具 CLI 路径')
    parser.add_argument('--output', help='私有输出父目录；每次创建独立子目录')
    parser.add_argument('--version')
    parser.add_argument('--desc', default='')
    args = parser.parse_args(argv)
    try:
        info = inspect_project(args.project)
        if args.action == 'inspect':
            print(json.dumps(info, ensure_ascii=False, indent=2))
            return 0
        if not args.output:
            raise ValueError('preview/upload 需要 --output 私有输出目录')
        if not info['appid'].startswith('wx'):
            raise ValueError('预览/上传需要实际小程序 AppID；请先核对账号，勿使用游客占位配置')
        if args.action == 'upload' and (not args.version or not args.version.strip()):
            raise ValueError('upload 需要非空 --version')
        cli = find_cli(args.cli)
        parent = Path(args.output).expanduser().resolve()
        parent.mkdir(parents=True, exist_ok=True)
        run = Path(tempfile.mkdtemp(prefix=args.action + '-', dir=str(parent)))
        cmd = [cli, args.action, '--project', info['project'], '--info-output', str(run / 'info.json')]
        if args.action == 'preview':
            cmd += ['--qr-format', 'image', '--qr-output', str(run / 'preview.jpg')]
        else:
            cmd += ['--version', args.version, '--desc', args.desc]
        print(f'本次结果目录：{run}', flush=True)
        # Arguments are passed without shell interpolation, even for spaces or metacharacters.
        result = subprocess.run(cmd, check=False)
        if result.returncode:
            print('开发者工具执行失败；先查看错误，不自动重试。', file=sys.stderr)
            return result.returncode if result.returncode > 0 else 1
        if args.action == 'preview':
            qr = run / 'preview.jpg'
            if not qr.is_file() or qr.stat().st_size == 0:
                raise ValueError('CLI 返回成功，但本次预览图片缺失；不要使用旧二维码，检查当前工具帮助和输出')
            print(f'开发预览图片：{qr}。这不是交付给体验成员的体验版二维码。')
        else:
            print('CLI 上传命令返回成功。请继续到正确账号后台核对版本、设为体验版、确认体验权限并交付体验码。')
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f'未完成：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
