"""Money / percent formatting and example tables used by content and the build."""
def money(v, cur='MYR', dec=2, lang='en'):
    neg = v < 0; a = abs(v)
    if cur == 'RUB':
        if lang == 'ru':
            # Russian typography: narrow non-breaking space as thousands sep, comma decimal, ₽ after
            s = f'{a:,.{dec}f}'.replace(',', '\u00a0').replace('.', ',')
            return ('−' if neg else '') + s + '\u00a0₽'
        return ('−' if neg else '') + f'{a:,.{dec}f} ₽'
    sym = {'MYR': 'RM', 'PHP': '₱', 'USD': '$', 'GBP': '£', 'SGD': 'S$', 'THB': '฿', 'EUR': '€'}.get(cur, cur + ' ')
    return ('−' if neg else '') + sym + f'{a:,.{dec}f}'

def pct(v):
    s = f'{v:.3f}'.rstrip('0').rstrip('.')
    return s + '%'

def ex_table(rows, total_label=None):
    """rows: list of (label, value_str, bold?)"""
    h = '<div class="tablewrap"><table><tbody>'
    for r in rows:
        lab, val = r[0], r[1]; b = len(r) > 2 and r[2]
        h += f'<tr><td>{"<b>" + lab + "</b>" if b else lab}</td><td class="n">{"<b>" + val + "</b>" if b else val}</td></tr>'
    return h + '</tbody></table></div>'
