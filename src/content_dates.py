"""Editorial content dates, independent of marketplace rate verification.

Dates are reviewed records, not the build clock or the last rate check. New
pages may omit modification metadata until an actual content date is recorded.
See content_dates.md for the historical baseline and update policy.
"""
import json
from datetime import date
from pathlib import Path

RECORDS = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))
for _path, _record in RECORDS.items():
    date.fromisoformat(_record['modified'])

_LABELS = {'en': 'Content updated', 'zh': '内容更新', 'ru': 'Контент обновлён', 'ms': 'Kandungan dikemas kini'}
_MONTHS = {
    'en': 'January February March April May June July August September October November December'.split(),
    'ms': 'Januari Februari Mac April Mei Jun Julai Ogos September Oktober November Disember'.split(),
    'ru': 'января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split(),
}


def modified(path):
    return RECORDS.get(path, {}).get('modified')


def label(lang):
    return _LABELS[lang]


def display(iso, lang):
    d = date.fromisoformat(iso)
    if lang == 'zh':
        return f'{d.year}年{d.month}月{d.day}日'
    return f'{d.day} {_MONTHS[lang][d.month - 1]} {d.year}'


def time_html(path, lang):
    iso = modified(path)
    if not iso:
        return ''
    return f'{label(lang)} <time datetime="{iso}">{display(iso, lang)}</time>'
