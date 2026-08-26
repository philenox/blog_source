"""Server-side SVG chart of the WHO weight-for-age distribution.

Produces a self-contained inline SVG showing the LMS-derived PDF at a
given (sex, age_days), with the user's weight marked and a few
reference percentile lines.
"""

import math

from .percentile import _load_table


# Standard normal quantiles for a few reference percentiles.
Z_P03 = -1.8807936081512509
Z_P97 = 1.8807936081512509


def _norm_pdf(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def _weight_at_z(L, M, S, z):
    """Invert the LMS z-score to a weight, or None if undefined."""
    if L == 0:
        return M * math.exp(z * S)
    inner = 1.0 + z * L * S
    if inner <= 0:
        return None
    return M * inner ** (1.0 / L)


def _pdf(L, M, S, x):
    """PDF of weight-for-age at x, via change-of-variables on the LMS z."""
    if x <= 0:
        return 0.0
    if L == 0:
        z = math.log(x / M) / S
        jacobian = 1.0 / (x * S)
    else:
        z = ((x / M) ** L - 1.0) / (L * S)
        jacobian = (x / M) ** (L - 1.0) / (M * S)
    return _norm_pdf(z) * jacobian


def _safe_z_range(L, M, S):
    """Widest safe z-range that keeps weight > 0 on both sides."""
    z_lo = -3.5
    while z_lo < -0.5:
        if _weight_at_z(L, M, S, z_lo) is not None:
            break
        z_lo += 0.1
    z_hi = 3.5
    while z_hi > 0.5:
        if _weight_at_z(L, M, S, z_hi) is not None:
            break
        z_hi -= 0.1
    return z_lo, z_hi


def render_pdf_svg(sex, age_days, user_weight_kg, n_points=180):
    """Return an inline SVG string of the weight PDF with the user marked.

    Colors and geometry are hard-coded to match the site's palette.
    """
    L, M, S = _load_table()[(sex, age_days)]

    z_lo, z_hi = _safe_z_range(L, M, S)
    w_min = _weight_at_z(L, M, S, z_lo)
    w_max = _weight_at_z(L, M, S, z_hi)

    # Widen slightly if the user's weight is off the default range.
    if user_weight_kg < w_min:
        w_min = user_weight_kg * 0.95
    if user_weight_kg > w_max:
        w_max = user_weight_kg * 1.05

    xs = [w_min + (w_max - w_min) * i / (n_points - 1) for i in range(n_points)]
    ys = [_pdf(L, M, S, x) for x in xs]
    pdf_max = max(ys)

    # Canvas geometry
    W, H = 520, 240
    pad_l, pad_r, pad_t, pad_b = 44, 16, 16, 42
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b

    def sx(w):
        return pad_l + (w - w_min) / (w_max - w_min) * plot_w

    def sy(p):
        return pad_t + plot_h - (p / pdf_max) * plot_h

    curve_pts = ' '.join(f'{sx(x):.1f},{sy(y):.1f}' for x, y in zip(xs, ys))
    baseline = pad_t + plot_h

    # Area under the curve up to the user's weight, as a shaded region.
    fill_pts = [f'{sx(w_min):.1f},{baseline:.1f}']
    for x, y in zip(xs, ys):
        if x <= user_weight_kg:
            fill_pts.append(f'{sx(x):.1f},{sy(y):.1f}')
        else:
            break
    fill_pts.append(f'{sx(min(user_weight_kg, w_max)):.1f},{baseline:.1f}')
    fill_path = ' '.join(fill_pts)

    # Reference percentile marks
    refs = []
    for label, z in (('3rd', Z_P03), ('50th', 0.0), ('97th', Z_P97)):
        rw = _weight_at_z(L, M, S, z)
        if rw is not None and w_min <= rw <= w_max:
            refs.append((label, rw, sx(rw)))

    # X-axis tick marks (roughly 5 ticks)
    n_ticks = 5
    tick_weights = [w_min + (w_max - w_min) * i / (n_ticks - 1) for i in range(n_ticks)]

    # User's marker
    user_x = sx(user_weight_kg)
    user_pdf = _pdf(L, M, S, user_weight_kg)
    user_y = sy(user_pdf)

    axis_color = '#888'
    curve_color = '#2c5aa0'
    fill_color = 'rgba(44, 90, 160, 0.18)'
    ref_color = '#bbb'
    ref_label_color = '#666'
    user_color = '#d9534f'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Weight distribution curve with your baby\'s '
        f'weight marked" style="width:100%; height:auto; max-width:{W}px;">',
        # Plot background
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" '
        f'fill="#fafafa" stroke="none" />',
        # Filled area under curve up to user's weight
        f'<polygon points="{fill_path}" fill="{fill_color}" stroke="none" />',
        # Reference percentile lines (behind the curve)
    ]
    for label, rw, rx in refs:
        parts.append(
            f'<line x1="{rx:.1f}" x2="{rx:.1f}" y1="{pad_t}" y2="{baseline}" '
            f'stroke="{ref_color}" stroke-width="1" stroke-dasharray="3,3" />'
        )
        parts.append(
            f'<text x="{rx:.1f}" y="{pad_t - 4}" text-anchor="middle" '
            f'font-size="10" fill="{ref_label_color}">{label}</text>'
        )
    # Distribution curve
    parts.append(
        f'<polyline points="{curve_pts}" fill="none" stroke="{curve_color}" '
        f'stroke-width="2" />'
    )
    # X-axis line
    parts.append(
        f'<line x1="{pad_l}" x2="{pad_l + plot_w}" y1="{baseline}" '
        f'y2="{baseline}" stroke="{axis_color}" stroke-width="1" />'
    )
    # X-axis ticks and labels
    for tw in tick_weights:
        tx = sx(tw)
        parts.append(
            f'<line x1="{tx:.1f}" x2="{tx:.1f}" y1="{baseline}" '
            f'y2="{baseline + 4}" stroke="{axis_color}" stroke-width="1" />'
        )
        parts.append(
            f'<text x="{tx:.1f}" y="{baseline + 16}" text-anchor="middle" '
            f'font-size="11" fill="#333">{tw:.1f} kg</text>'
        )
    # X-axis title
    parts.append(
        f'<text x="{pad_l + plot_w / 2:.1f}" y="{H - 6}" text-anchor="middle" '
        f'font-size="11" fill="#555">Weight (kg)</text>'
    )
    # User's vertical marker + dot + label
    parts.append(
        f'<line x1="{user_x:.1f}" x2="{user_x:.1f}" y1="{user_y:.1f}" '
        f'y2="{baseline}" stroke="{user_color}" stroke-width="2" />'
    )
    parts.append(
        f'<circle cx="{user_x:.1f}" cy="{user_y:.1f}" r="4.5" '
        f'fill="{user_color}" stroke="white" stroke-width="1.5" />'
    )
    # Baby weight label above the dot, kept inside plot area
    label_y = max(pad_t + 12, user_y - 8)
    label_anchor = 'middle'
    if user_x < pad_l + 32:
        label_anchor = 'start'
    elif user_x > pad_l + plot_w - 32:
        label_anchor = 'end'
    parts.append(
        f'<text x="{user_x:.1f}" y="{label_y:.1f}" text-anchor="{label_anchor}" '
        f'font-size="11" font-weight="bold" fill="{user_color}">'
        f'{user_weight_kg:g} kg</text>'
    )
    parts.append('</svg>')
    return '\n'.join(parts)
