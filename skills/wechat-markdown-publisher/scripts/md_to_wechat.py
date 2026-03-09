#!/usr/bin/env python3
import argparse
import base64
import html
import mimetypes
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

THEMES = {
    'wechat': {
        'container': 'max-width:100%;margin:0 auto;padding:24px 20px 48px 20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.75;color:#333333;word-wrap:break-word;background-color:#ffffff;',
        'h1': 'font-size:32px;font-weight:700;color:#111;line-height:1.3;margin:38px 0 16px;letter-spacing:-0.015em;text-align:center;',
        'h2': 'font-size:26px;font-weight:600;color:#111;line-height:1.35;margin:32px 0 16px;padding-left:12px;border-left:4px solid #07c160;',
        'h3': 'font-size:21px;font-weight:600;color:#333333;line-height:1.4;margin:28px 0 14px;',
        'p': 'margin:18px 0;line-height:1.75;color:#333333;text-align:justify;',
        'strong': 'font-weight:700;color:#07c160;background-color:rgba(7,193,96,0.08);padding:0 4px;border-radius:4px;',
        'em': 'font-style:italic;color:#666666;',
        'blockquote': 'margin:24px 0;padding:16px 20px;background-color:#f0f7f2;border-left:4px solid #07c160;color:#555555;border-radius:4px;',
        'ul': 'margin:16px 0;padding-left:28px;list-style-type:disc;list-style-position:outside;',
        'ol': 'margin:16px 0;padding-left:28px;list-style-type:decimal;list-style-position:outside;',
        'li': 'margin:8px 0;line-height:1.75;color:#333333;',
        'code': 'font-family:"SF Mono",Consolas,monospace;padding:3px 6px;background-color:#f0f7f2;color:#07c160;border-radius:4px;font-size:12px;line-height:1.5;',
        'pre': 'margin:24px 0;padding:20px;background-color:#f0f7f2;border-radius:8px;overflow-x:auto;font-size:12px;line-height:1.5;color:#24292e;',
        'a': 'color:#07c160;text-decoration:none;border-bottom:1px solid #07c160;padding-bottom:1px;word-break:break-all;',
        'img': 'max-width:100%;height:auto;display:block;margin:24px auto;border-radius:8px;',
        'hr': 'margin:36px auto;border:none;height:1px;background-color:#eaeaea;width:100%;',
        'table': 'width:100%;margin:24px 0;border-collapse:collapse;font-size:15px;',
        'th': 'background-color:#f0f7f2;padding:12px 16px;text-align:left;font-weight:600;color:#333333;border:1px solid #d8e8dc;',
        'td': 'padding:12px 16px;border:1px solid #d8e8dc;color:#333333;vertical-align:top;',
    },
    'notion': {
        'container': 'max-width:100%;margin:0 auto;padding:24px 20px 48px 20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.6;color:#37352f;word-wrap:break-word;background-color:#ffffff;',
        'h1': 'font-size:34px;font-weight:700;color:#37352f;line-height:1.2;margin:38px 0 8px;letter-spacing:-0.02em;',
        'h2': 'font-size:26px;font-weight:600;color:#37352f;line-height:1.3;margin:32px 0 8px;',
        'h3': 'font-size:21px;font-weight:600;color:#37352f;line-height:1.35;margin:28px 0 8px;',
        'p': 'margin:8px 0;line-height:1.6;color:#37352f;text-align:justify;',
        'strong': 'font-weight:700;color:#37352f;',
        'em': 'font-style:italic;color:#37352f;',
        'blockquote': 'margin:8px 0;padding:4px 16px;background-color:transparent;border-left:3px solid #37352f;color:#37352f;',
        'ul': 'margin:4px 0;padding-left:26px;list-style-type:disc;list-style-position:outside;',
        'ol': 'margin:4px 0;padding-left:26px;list-style-type:decimal;list-style-position:outside;',
        'li': 'margin:2px 0;line-height:1.6;color:#37352f;',
        'code': 'font-family:"SF Mono",Consolas,monospace;padding:2px 5px;background-color:#f7f6f3;color:#eb5757;border-radius:3px;font-size:13px;line-height:1.5;',
        'pre': 'margin:16px 0;padding:20px;background-color:#f7f6f3;border-radius:4px;overflow-x:auto;font-size:13px;line-height:1.5;color:#24292e;',
        'a': 'color:#37352f;text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(55,53,47,0.4);word-break:break-all;',
        'img': 'max-width:100%;height:auto;display:block;margin:16px auto;border-radius:4px;',
        'hr': 'margin:24px auto;border:none;height:1px;background-color:#e9e9e7;width:100%;',
        'table': 'width:100%;margin:16px 0;border-collapse:collapse;font-size:15px;',
        'th': 'background-color:#f7f6f3;padding:8px 12px;text-align:left;font-weight:600;color:#37352f;border:1px solid #e9e9e7;',
        'td': 'padding:8px 12px;border:1px solid #e9e9e7;color:#37352f;vertical-align:top;',
    },
    'claude': {
        'container': 'max-width:100%;margin:0 auto;padding:24px 20px 48px 20px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.7;color:#2b2b2b;word-wrap:break-word;background-color:#f8f6f0;',
        'h1': 'font-size:32px;font-weight:700;color:#b75c3d;line-height:1.3;margin:38px 0 16px;letter-spacing:-0.015em;text-align:center;',
        'h2': 'font-size:26px;font-weight:600;color:#b75c3d;line-height:1.35;margin:32px 0 16px;',
        'h3': 'font-size:21px;font-weight:600;color:#2b2b2b;line-height:1.4;margin:28px 0 14px;',
        'p': 'margin:18px 0;line-height:1.7;color:#2b2b2b;text-align:justify;',
        'strong': 'font-weight:700;color:#b75c3d;background-color:rgba(183,92,61,0.08);padding:0 4px;border-radius:4px;',
        'em': 'font-style:italic;color:#666666;',
        'blockquote': 'margin:24px 0;padding:16px 20px;background-color:rgba(183,92,61,0.04);border-left:4px solid #b75c3d;color:#555555;border-radius:4px;',
        'ul': 'margin:16px 0;padding-left:28px;list-style-type:disc;list-style-position:outside;',
        'ol': 'margin:16px 0;padding-left:28px;list-style-type:decimal;list-style-position:outside;',
        'li': 'margin:8px 0;line-height:1.7;color:#2b2b2b;',
        'code': 'font-family:"SF Mono",Consolas,monospace;padding:3px 6px;background-color:#f0ece4;color:#b75c3d;border-radius:4px;font-size:12px;line-height:1.5;',
        'pre': 'margin:24px 0;padding:20px;background-color:#f0ece4;border-radius:8px;overflow-x:auto;font-size:12px;line-height:1.5;color:#24292e;',
        'a': 'color:#b75c3d;text-decoration:none;border-bottom:1px solid #b75c3d;padding-bottom:1px;word-break:break-all;',
        'img': 'max-width:100%;height:auto;display:block;margin:24px auto;border-radius:8px;',
        'hr': 'margin:36px auto;border:none;height:1px;background-color:#eaeaea;width:100%;',
        'table': 'width:100%;margin:24px 0;border-collapse:collapse;font-size:15px;',
        'th': 'background-color:#f0ece4;padding:12px 16px;text-align:left;font-weight:600;color:#2b2b2b;border:1px solid #e0ddd6;',
        'td': 'padding:12px 16px;border:1px solid #e0ddd6;color:#2b2b2b;vertical-align:top;',
    }
}


def theme(name: str):
    return THEMES.get(name, THEMES['wechat'])


def escape_text(s: str) -> str:
    return html.escape(s, quote=False)


def apply_inline(text: str) -> str:
    text = escape_text(text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]+)")?\)',
                  lambda m: f'<img src="{html.escape(m.group(2), quote=True)}" alt="{html.escape(m.group(1), quote=True)}" />', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]+)")?\)',
                  lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', text)
    text = re.sub(r'`([^`]+)`', lambda m: f'<code>{m.group(1)}</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', text)
    return text


def split_table_row(line: str):
    if '|' not in line:
        return None
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def render_list(items, ordered=False):
    tag = 'ol' if ordered else 'ul'
    body = ''.join(f'<li>{apply_inline(item)}</li>' for item in items)
    return f'<{tag}>{body}</{tag}>'


def render_table(rows):
    if not rows:
        return ''
    header = rows[0]
    body_rows = rows[2:] if len(rows) > 1 and all(re.match(r'^:?-{3,}:?$', c.strip()) for c in rows[1]) else rows[1:]
    thead = '<tr>' + ''.join(f'<th>{apply_inline(c)}</th>' for c in header) + '</tr>'
    tbody = ''.join('<tr>' + ''.join(f'<td>{apply_inline(c)}</td>' for c in row) + '</tr>' for row in body_rows)
    return f'<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>'


def markdown_to_html(md: str, title: str | None = None) -> str:
    lines = md.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    out = []
    para = []
    quote_buf = []
    list_items = []
    list_ordered = False
    table_rows = []
    in_code = False
    code_lines = []

    def flush_paragraph():
        nonlocal para
        if not para:
            return
        text = ' '.join(x.strip() for x in para if x.strip())
        if text:
            out.append(f'<p>{apply_inline(text)}</p>')
        para = []

    def flush_quote():
        nonlocal quote_buf
        if quote_buf:
            content = '<br/>'.join(apply_inline(x.strip()) for x in quote_buf if x.strip())
            out.append(f'<blockquote>{content}</blockquote>')
            quote_buf = []

    def flush_list():
        nonlocal list_items, list_ordered
        if list_items:
            out.append(render_list(list_items, ordered=list_ordered))
            list_items = []
            list_ordered = False

    def flush_table():
        nonlocal table_rows
        if table_rows:
            out.append(render_table(table_rows))
            table_rows = []

    for raw in lines:
        line = raw.rstrip()

        if in_code:
            if line.startswith('```'):
                code = '\n'.join(code_lines)
                dots = '<div data-code-head="1"><span></span><span></span><span></span></div>'
                out.append(f'<pre>{dots}<code>{html.escape(code)}</code></pre>')
                in_code = False
                code_lines = []
            else:
                code_lines.append(raw)
            continue

        if line.startswith('```'):
            flush_paragraph(); flush_quote(); flush_list(); flush_table()
            in_code = True
            code_lines = []
            continue

        if not line.strip():
            flush_paragraph(); flush_quote(); flush_list(); flush_table()
            continue

        row = split_table_row(line)
        if row and len(row) >= 2:
            flush_paragraph(); flush_quote(); flush_list()
            table_rows.append(row)
            continue
        else:
            flush_table()

        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_paragraph(); flush_quote(); flush_list(); flush_table()
            level = min(len(m.group(1)), 3)
            out.append(f'<h{level}>{apply_inline(m.group(2).strip())}</h{level}>')
            continue

        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', line.strip()):
            flush_paragraph(); flush_quote(); flush_list(); flush_table()
            out.append('<hr/>')
            continue

        if line.lstrip().startswith('>'):
            flush_paragraph(); flush_list(); flush_table()
            quote_buf.append(re.sub(r'^\s*>\s?', '', line))
            continue
        else:
            flush_quote()

        m_ul = re.match(r'^\s*[-*+]\s+(.*)$', line)
        m_ol = re.match(r'^\s*\d+\.\s+(.*)$', line)
        if m_ul or m_ol:
            flush_paragraph(); flush_table()
            item = (m_ul or m_ol).group(1).strip()
            ordered = bool(m_ol)
            if list_items and list_ordered != ordered:
                flush_list()
            list_ordered = ordered
            list_items.append(item)
            continue
        else:
            flush_list()

        if re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip()):
            flush_paragraph(); flush_table()
            out.append(apply_inline(line.strip()))
            continue

        para.append(line)

    flush_paragraph(); flush_quote(); flush_list(); flush_table()
    if in_code:
        code = '\n'.join(code_lines)
        out.append(f'<pre><code>{html.escape(code)}</code></pre>')
    if title and not re.search(r'<h1>.*?</h1>', ''.join(out), flags=re.S):
        out.insert(0, f'<h1>{apply_inline(title)}</h1>')
    return ''.join(out)


def as_data_uri_from_bytes(data: bytes, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(data).decode('ascii')


def convert_images_to_base64(html_text: str, base_dir: Path) -> str:
    pattern = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)("[^>]*>)', re.I)

    def repl(m):
        prefix, src, suffix = m.groups()
        if src.startswith('data:'):
            return m.group(0)
        try:
            if re.match(r'^https?://', src, re.I):
                req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = resp.read()
                    mime = resp.headers.get_content_type() or mimetypes.guess_type(src)[0] or 'image/png'
                    return prefix + as_data_uri_from_bytes(data, mime) + suffix
            parsed = urllib.parse.urlparse(src)
            if parsed.scheme == '' and not src.startswith('//'):
                fp = (base_dir / src).resolve()
                if fp.exists() and fp.is_file():
                    data = fp.read_bytes()
                    mime = mimetypes.guess_type(fp.name)[0] or 'image/png'
                    return prefix + as_data_uri_from_bytes(data, mime) + suffix
        except Exception:
            return m.group(0)
        return m.group(0)

    return pattern.sub(repl, html_text)


def attr_escape(s: str) -> str:
    return s.replace('"', '&quot;')


def apply_tag_style(html_text: str, tag: str, style: str, skip_if_has_style: bool = False) -> str:
    pattern = re.compile(fr'<{tag}(\s[^>]*?)?(\s*/?)>', re.I)

    def repl(m):
        attrs = m.group(1) or ''
        closing = m.group(2) or ''
        if skip_if_has_style and re.search(r'\bstyle\s*=', attrs, re.I):
            return m.group(0)
        escaped_style = attr_escape(style)
        if re.search(r'\bstyle\s*=\s*"([^"]*)"', attrs, re.I):
            attrs = re.sub(
                r'style\s*=\s*"([^"]*)"',
                lambda x: f'style="{attr_escape(x.group(1).rstrip(";") + ";" + style)}"',
                attrs,
                flags=re.I,
            )
            return f'<{tag}{attrs}{closing}>'
        if re.search(r"\bstyle\s*=\s*'([^']*)'", attrs, re.I):
            attrs = re.sub(
                r"style\s*=\s*'([^']*)'",
                lambda x: f'style="{attr_escape(x.group(1).rstrip(";") + ";" + style)}"',
                attrs,
                flags=re.I,
            )
            return f'<{tag}{attrs}{closing}>'
        return f'<{tag}{attrs} style="{escaped_style}"{closing}>'

    return pattern.sub(repl, html_text)


def add_inline_styles(html_text: str, theme_name: str) -> str:
    t = theme(theme_name)
    html_text = apply_tag_style(html_text, 'h1', t['h1'])
    html_text = apply_tag_style(html_text, 'h2', t['h2'])
    html_text = apply_tag_style(html_text, 'h3', t['h3'])
    html_text = apply_tag_style(html_text, 'p', t['p'])
    html_text = apply_tag_style(html_text, 'blockquote', t['blockquote'])
    html_text = apply_tag_style(html_text, 'ul', t['ul'])
    html_text = apply_tag_style(html_text, 'ol', t['ol'])
    html_text = apply_tag_style(html_text, 'li', t['li'])
    html_text = apply_tag_style(html_text, 'code', t['code'], skip_if_has_style=False)
    html_text = apply_tag_style(html_text, 'pre', t['pre'])
    html_text = apply_tag_style(html_text, 'a', t['a'])
    html_text = apply_tag_style(html_text, 'img', t['img'])
    html_text = apply_tag_style(html_text, 'hr', t['hr'])
    html_text = apply_tag_style(html_text, 'table', t['table'])
    html_text = apply_tag_style(html_text, 'th', t['th'])
    html_text = apply_tag_style(html_text, 'td', t['td'])
    html_text = apply_tag_style(html_text, 'strong', t['strong'])
    html_text = apply_tag_style(html_text, 'em', t['em'])
    html_text = re.sub(r'<div data-code-head="1">\s*<span></span><span></span><span></span>\s*</div>',
                       '<div style="margin-bottom:12px;white-space:nowrap;"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#ff5f56;margin-right:6px;"></span><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#ffbd2e;margin-right:6px;"></span><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#27c93f;"></span></div>', html_text)
    html_text = re.sub(r'<pre([^>]*)><code([^>]*)>', r'<pre\1><code\2 style="background:transparent;padding:0;border-radius:0;color:inherit;">', html_text)
    return html_text


def group_consecutive_images_to_table(html_text: str) -> str:
    pattern = re.compile(r'((?:<img\b[^>]*>\s*){2,})', re.I)

    def normalize_img(img: str) -> str:
        m = re.search(r'style="([^"]*)"', img, flags=re.I)
        extra = 'width:100% !important;display:block;margin:0 auto;'
        if m:
            style = attr_escape(m.group(1).rstrip(';') + ';' + extra)
            return re.sub(r'style="([^"]*)"', f'style="{style}"', img, count=1, flags=re.I)
        return re.sub(r'\s*/?>$', f' style="{attr_escape(extra)}" />', img, count=1, flags=re.I)

    def repl(m):
        imgs = re.findall(r'<img\b[^>]*>', m.group(1), flags=re.I)
        if len(imgs) < 2:
            return m.group(1)
        cells = ''.join(
            f'<td style="padding:0 4px;vertical-align:top;border:none;background:transparent;">{normalize_img(img)}</td>'
            for img in imgs
        )
        return f'<table style="width:100%;border-collapse:collapse;margin:16px 0;border:none !important;"><tbody><tr style="border:none !important;background:transparent !important;">{cells}</tr></tbody></table>'

    return pattern.sub(repl, html_text)


def flatten_list_paragraphs(html_text: str) -> str:
    html_text = re.sub(r'<li([^>]*)>\s*<p[^>]*>(.*?)</p>\s*</li>', r'<li\1>\2</li>', html_text, flags=re.I | re.S)
    return html_text


def keep_cjk_punctuation_tight(html_text: str) -> str:
    return re.sub(r'(</(?:strong|b|em|span|a|code)>)\s*([：；，。！？、:])', r'\1&#8288;\2', html_text)


def build_final_html(inner_html: str, theme_name: str) -> str:
    container = attr_escape(theme(theme_name)['container'])
    return f'<section style="{container}">{inner_html}</section>'


def make_wechat_compatible(html_text: str, theme_name: str) -> str:
    html_text = add_inline_styles(html_text, theme_name)
    html_text = flatten_list_paragraphs(html_text)
    html_text = group_consecutive_images_to_table(html_text)
    html_text = keep_cjk_punctuation_tight(html_text)
    html_text = build_final_html(html_text, theme_name)
    return html_text


def copy_clipboard(text: str):
    candidates = [['pbcopy'], ['wl-copy'], ['xclip', '-selection', 'clipboard'], ['xsel', '--clipboard', '--input']]
    for cmd in candidates:
        try:
            p = subprocess.run(cmd, input=text.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.returncode == 0:
                return True, 'clipboard:' + cmd[0]
        except FileNotFoundError:
            pass
        except Exception:
            pass
    try:
        if sys.stdout.isatty():
            encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
            sys.stdout.write(f'\033]52;c;{encoded}\a')
            sys.stdout.flush()
            return True, 'clipboard:osc52'
    except Exception:
        pass
    return False, 'no-clipboard-backend'


def main():
    ap = argparse.ArgumentParser(description='Convert Markdown to WeChat-friendly HTML.')
    ap.add_argument('input', help='Input markdown file')
    ap.add_argument('--output', '-o', help='Output HTML file')
    ap.add_argument('--title', help='Optional title if markdown has no H1')
    ap.add_argument('--copy', action='store_true', help='Try copying HTML to clipboard')
    ap.add_argument('--theme', default='wechat', choices=sorted(THEMES.keys()), help='Theme preset')
    ap.add_argument('--embed-images', action='store_true', help='Convert image src to base64 when possible')
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f'ERROR: input file not found: {src}', file=sys.stderr)
        sys.exit(2)

    md = src.read_text(encoding='utf-8')
    title = args.title or src.stem.replace('_', ' ').replace('-', ' ')
    html_text = markdown_to_html(md, title=title)
    if args.embed_images:
        html_text = convert_images_to_base64(html_text, src.parent)
    html_text = make_wechat_compatible(html_text, args.theme)

    out_path = Path(args.output) if args.output else src.with_suffix('.wechat.html')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding='utf-8')

    copied = False
    backend = None
    if args.copy:
        copied, backend = copy_clipboard(html_text)

    print(f'INPUT={src}')
    print(f'OUTPUT={out_path}')
    print(f'THEME={args.theme}')
    print(f'EMBED_IMAGES={str(bool(args.embed_images)).lower()}')
    print(f'COPIED={str(copied).lower()}')
    if backend:
        print(f'COPY_BACKEND={backend}')


if __name__ == '__main__':
    main()
