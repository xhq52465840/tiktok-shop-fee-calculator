def money(v, cur='MYR', dec=2):
    sym = {'MYR': 'RM', 'PHP': '₱', 'USD': '$', 'GBP': '£'}.get(cur, cur + ' ')
    return ('−' if v < 0 else '') + sym + f"{abs(v):,.{dec}f}"
def pct(v):
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return s + '%'
def ex_table(rows, total_label=None):
    """rows: list of (label, value_str, bold?)"""
    h = '<div class="tablewrap"><table><tbody>'
    for r in rows:
        lab, val = r[0], r[1]; b = len(r) > 2 and r[2]
        h += f'<tr><td>{"<b>" + lab + "</b>" if b else lab}</td><td class="n">{"<b>" + val + "</b>" if b else val}</td></tr>'
    return h + '</tbody></table></div>'
