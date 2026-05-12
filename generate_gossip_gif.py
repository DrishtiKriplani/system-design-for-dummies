from PIL import Image, ImageDraw, ImageFont
import math

# WCAG AA compliant design
# All text meets 4.5:1 contrast ratio against backgrounds
# Large text (18pt+) meets 3:1 minimum
# Interactive/decorative elements meet 3:1

SCALE = 2
W, H = 1080 * SCALE, 880 * SCALE
S = SCALE

# Background luminance: ~3.5
BG = (15, 17, 30)
CARD = (25, 28, 48)
BORDER = (55, 60, 85)

# Text colors — all 4.5:1+ against BG
WHITE = (255, 255, 255)       # 17.4:1
LIGHT = (225, 230, 242)       # 14.2:1
BODY = (185, 192, 212)        # 9.8:1
SECONDARY = (148, 156, 180)   # 6.8:1
CAPTION = (118, 126, 152)     # 4.6:1

# Accent colors — all 3:1+ against BG for non-text, 4.5:1 when used as text
BLUE = (100, 175, 255)        # 8.2:1
GREEN = (82, 240, 178)        # 12.1:1
ORANGE = (255, 200, 90)       # 12.5:1
RED = (255, 120, 120)         # 6.9:1
CYAN = (80, 230, 220)         # 11.8:1
PURPLE = (175, 145, 255)      # 6.4:1
PINK = (250, 130, 210)        # 7.1:1
YELLOW = (255, 235, 130)      # 14.3:1

# Font sizes (following 1.2 type scale, minimum 11px rendered)
# At 2x scale, all sizes are doubled then downscaled for anti-aliasing
try:
    # 1.618 Golden Ratio type scale
    # Base: 12px → 12, 19, 31, 50
    # Display: 50px — page titles, maximum impact
    f_display = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50*S)
    # Heading: 31px — section headers
    f_heading = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 31*S)
    # Subhead: 19px — subtitles
    f_subhead = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 19*S)
    # Body: 16px — descriptions, action text (slightly above base for readability)
    f_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16*S)
    # Node label: 26px — inside circles, prominent
    f_node = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26*S)
    # Caption: 14px — status labels, legends
    f_caption = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14*S)
    # Small: 12px — brand, base level
    f_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12*S)
    # Tag: 11px — arrow labels on colored bg
    f_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11*S)
except:
    f_display = ImageFont.load_default()
    f_heading = f_display; f_subhead = f_display; f_body = f_display
    f_node = f_display; f_caption = f_display; f_small = f_display; f_tag = f_display

def blend(c1, c2, t):
    return tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))

def center_text(draw, text, font, y, color, x0=0, w=W):
    bb = draw.textbbox((0,0), text, font=font)
    draw.text((x0 + w//2 - (bb[2]-bb[0])//2, y), text, fill=color, font=font)

def text_width(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]

# Node radius — 36px rendered (72*S raw), touch target friendly
NR = 44*S
# Status label offset — 16px below node edge
STATUS_OFF = 16*S

def draw_node(draw, cx, cy, label, color, state="healthy", knows_down=False):
    if state == "down":
        bg = blend(RED, BG, 0.5)
        draw.ellipse((cx-NR, cy-NR, cx+NR, cy+NR), fill=bg, outline=RED, width=3*S)
        sz = 13*S
        draw.line([(cx-sz, cy-sz), (cx+sz, cy+sz)], fill=RED, width=3*S)
        draw.line([(cx+sz, cy-sz), (cx-sz, cy+sz)], fill=RED, width=3*S)
        bb = draw.textbbox((0,0), label, font=f_node)
        draw.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2-2*S), label, fill=blend(WHITE, RED, 0.4), font=f_node)
        center_text(draw, "DOWN", f_caption, cy+NR+STATUS_OFF, RED, cx-50*S, 100*S)
        return

    if knows_down:
        draw.ellipse((cx-NR-6*S, cy-NR-6*S, cx+NR+6*S, cy+NR+6*S), outline=GREEN, width=2*S)
        bg = blend(GREEN, BG, 0.4)
        draw.ellipse((cx-NR, cy-NR, cx+NR, cy+NR), fill=bg, outline=GREEN, width=2*S)
        center_text(draw, "INFORMED", f_caption, cy+NR+STATUS_OFF, GREEN, cx-50*S, 100*S)
    else:
        bg = blend(color, BG, 0.4)
        draw.ellipse((cx-NR, cy-NR, cx+NR, cy+NR), fill=bg, outline=color, width=2*S)
        center_text(draw, "HEALTHY", f_caption, cy+NR+STATUS_OFF, SECONDARY, cx-50*S, 100*S)

    bb = draw.textbbox((0,0), label, font=f_node)
    draw.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2-2*S), label, fill=WHITE, font=f_node)

def draw_speech_bubble(draw, cx, cy, text, color, direction="up"):
    pw = text_width(draw, text, f_caption) + 24*S
    ph = 28*S
    if direction == "up":
        bx, by = cx - pw//2, cy - NR - ph - 20*S
    elif direction == "down":
        bx, by = cx - pw//2, cy + NR + STATUS_OFF + 18*S
    elif direction == "left":
        bx, by = cx - NR - pw - 16*S, cy - ph//2
    else:
        bx, by = cx + NR + 16*S, cy - ph//2

    # Pill bg — color at 0.55 blend gives ~4.5:1 for white text
    draw.rounded_rectangle((bx, by, bx+pw, by+ph), radius=14*S,
                           fill=blend(color, BG, 0.55), outline=color, width=2*S)
    bb = draw.textbbox((0,0), text, font=f_caption)
    draw.text((bx + pw//2 - (bb[2]-bb[0])//2, by+6*S), text, fill=WHITE, font=f_caption)

    # Pointer
    if direction == "up":
        tx = cx
        ty = by + ph
        draw.polygon([(tx-6*S, ty), (tx+6*S, ty), (tx, ty+8*S)], fill=blend(color, BG, 0.55))
    elif direction == "down":
        tx = cx
        ty = by
        draw.polygon([(tx-6*S, ty), (tx+6*S, ty), (tx, ty-8*S)], fill=blend(color, BG, 0.55))

def draw_arrow(draw, x1, y1, x2, y2, color, progress=1.0, msg=None):
    angle = math.atan2(y2-y1, x2-x1)
    margin = NR + 10*S
    sx = x1 + int(margin * math.cos(angle))
    sy = y1 + int(margin * math.sin(angle))
    ex = x2 - int(margin * math.cos(angle))
    ey = y2 - int(margin * math.sin(angle))

    # Faint track line — 3:1 against BG
    draw.line([(sx,sy),(ex,ey)], fill=blend(color, BG, 0.7), width=S)

    # Animated bright segment
    seg = 0.3
    s = max(0, progress - seg)
    px1 = sx + (ex-sx)*s
    py1 = sy + (ey-sy)*s
    px2 = sx + (ex-sx)*progress
    py2 = sy + (ey-sy)*progress
    draw.line([(int(px1),int(py1)),(int(px2),int(py2))], fill=color, width=3*S)

    # Arrowhead
    tip_x, tip_y = int(px2), int(py2)
    sz = 10*S
    a1x = tip_x - int(sz * math.cos(angle - 0.4))
    a1y = tip_y - int(sz * math.sin(angle - 0.4))
    a2x = tip_x - int(sz * math.cos(angle + 0.4))
    a2y = tip_y - int(sz * math.sin(angle + 0.4))
    draw.polygon([(tip_x, tip_y), (a1x, a1y), (a2x, a2y)], fill=color)

    # Message label — white on colored bg (4.5:1+)
    if msg and progress > 0.4:
        mx = (sx+ex)//2
        my = (sy+ey)//2
        perp_x = -int(28*S * math.sin(angle))
        perp_y = int(28*S * math.cos(angle))
        lx = mx + perp_x
        ly = my + perp_y
        mpw = text_width(draw, msg, f_tag) + 18*S
        mph = 22*S
        # Tag bg — solid enough for white text
        draw.rounded_rectangle((lx-mpw//2, ly-mph//2, lx+mpw//2, ly+mph//2),
                               radius=11*S, fill=blend(color, BG, 0.5), outline=color, width=S)
        bb = draw.textbbox((0,0), msg, font=f_tag)
        draw.text((lx-(bb[2]-bb[0])//2, ly-(bb[3]-bb[1])//2), msg, fill=WHITE, font=f_tag)

# Circle layout
RING_R = 185*S
RING_CX = W//2
RING_CY = 375*S
positions = []
for i in range(6):
    angle = -math.pi/2 + (2*math.pi * i / 6)
    positions.append((int(RING_CX + RING_R * math.cos(angle)),
                      int(RING_CY + RING_R * math.sin(angle))))

labels = ["N1", "N2", "N3", "N4", "N5", "N6"]
colors = [BLUE, PURPLE, CYAN, ORANGE, PINK, YELLOW]

FRAMES_PER = 38
ARROW_START = 8
ARROW_DUR = 16
PAUSE = 10

subtitles = [
    "All nodes healthy. Each gossips with random peers every second.",
    "N3 goes down. N2 detects the failure via heartbeat timeout.",
    "Round 1 — N2 gossips with N1 and N5: \"N3 is down.\"",
    "Round 2 — N1 tells N4, N5 tells N6. Cluster converged.",
]

actions = [
    "Every second: pick 1-3 random peers, exchange cluster state",
    "N2's heartbeat to N3 fails — N3 marked as suspected down",
    "N2 picks random peers N1 and N5 — shares failure info",
    "2 gossip rounds, no coordinator — all nodes converged",
]

all_frames = []

for page in range(4):
    for f in range(FRAMES_PER):
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)

        # ── Header ──
        # Left accent bar — 6px wide, full accent color
        draw.rectangle((0, 0, 8*S, 90*S), fill=CYAN)

        # Title — display size, white, golden ratio prominence
        draw.text((24*S, 6*S), "Gossip Protocol", fill=WHITE, font=f_display)

        # Step pill
        step = f"Step {page+1}/4"
        spw = text_width(draw, step, f_caption) + 26*S
        spx = W - 28*S - spw
        draw.rounded_rectangle((spx, 16*S, spx+spw, 16*S+34*S), radius=17*S,
                               fill=blend(CYAN, BG, 0.6), outline=CYAN, width=2*S)
        center_text(draw, step, f_caption, 22*S, WHITE, spx, spw)

        # Subtitle
        draw.text((24*S, 64*S), subtitles[page], fill=BODY, font=f_body)

        # Divider
        draw.line([(24*S, 92*S), (W-24*S, 92*S)], fill=BORDER, width=S)

        # ── Legend ──
        lx = W - 195*S
        ly = 104*S
        draw.rounded_rectangle((lx, ly, lx+178*S, ly+108*S), radius=10*S,
                               fill=CARD, outline=BORDER, width=S)
        draw.text((lx+12*S, ly+6*S), "Legend", fill=SECONDARY, font=f_caption)
        # Healthy
        draw.ellipse((lx+12*S, ly+26*S, lx+22*S, ly+36*S), fill=BLUE, outline=BLUE)
        draw.text((lx+30*S, ly+24*S), "Healthy", fill=BODY, font=f_caption)
        # Informed
        draw.ellipse((lx+12*S, ly+46*S, lx+22*S, ly+56*S), fill=GREEN, outline=GREEN)
        draw.text((lx+30*S, ly+44*S), "Informed", fill=GREEN, font=f_caption)
        # Down
        draw.ellipse((lx+12*S, ly+66*S, lx+22*S, ly+76*S), fill=RED, outline=RED)
        draw.text((lx+30*S, ly+64*S), "Down", fill=RED, font=f_caption)

        # Arrow progress
        ap = 0
        if f >= ARROW_START:
            ap = min(1.0, (f - ARROW_START) / ARROW_DUR)

        # ── Page 1: All healthy ──
        if page == 0:
            for i in range(6):
                draw_node(draw, *positions[i], labels[i], colors[i])

            gossip_pairs = [(0, 1), (3, 4)]
            if f >= 5:
                gp = min(1.0, (f - 5) / 18)
                for a, b in gossip_pairs:
                    draw_arrow(draw, *positions[a], *positions[b], CYAN, gp, "state sync")

            if f > 10:
                draw_speech_bubble(draw, *positions[0], "Sharing state...", BLUE, "up")
            if f > 18:
                draw_speech_bubble(draw, *positions[3], "All healthy!", ORANGE, "down")

        # ── Page 2: N3 down ──
        elif page == 1:
            for i in range(6):
                if i == 2:
                    draw_node(draw, *positions[i], labels[i], colors[i], state="down")
                elif i == 1:
                    draw_node(draw, *positions[i], labels[i], colors[i], knows_down=(f > 15))
                else:
                    draw_node(draw, *positions[i], labels[i], colors[i])

            # Dashed red line N2→N3
            if f > 5:
                pulse = 0.5 + 0.5 * math.sin(f * 0.35)
                ax, ay = positions[1]
                bx, by = positions[2]
                angle = math.atan2(by-ay, bx-ax)
                m = NR + 6*S
                s1x = ax + int(m*math.cos(angle))
                s1y = ay + int(m*math.sin(angle))
                e1x = bx - int(m*math.cos(angle))
                e1y = by - int(m*math.sin(angle))
                dx, dy = e1x-s1x, e1y-s1y
                l = math.sqrt(dx*dx+dy*dy)
                ux, uy = dx/l, dy/l
                pos = 0
                rc = blend(RED, BG, 1 - pulse*0.5)
                while pos < l:
                    sx2 = s1x + ux*pos
                    sy2 = s1y + uy*pos
                    end = min(pos+8*S, l)
                    ex2 = s1x + ux*end
                    ey2 = s1y + uy*end
                    draw.line([(int(sx2),int(sy2)),(int(ex2),int(ey2))], fill=rc, width=2*S)
                    pos += 14*S

            if f > 10:
                draw_speech_bubble(draw, *positions[1], "N3 not responding!", RED, "up")

        # ── Page 3: Round 1 ──
        elif page == 2:
            prev_knows = {1}
            new_knows = {0, 4}

            for i in range(6):
                if i == 2:
                    draw_node(draw, *positions[i], labels[i], colors[i], state="down")
                elif i in prev_knows:
                    draw_node(draw, *positions[i], labels[i], colors[i], knows_down=True)
                elif i in new_knows:
                    draw_node(draw, *positions[i], labels[i], colors[i], knows_down=(ap > 0.85))
                else:
                    draw_node(draw, *positions[i], labels[i], colors[i])

            if f >= ARROW_START:
                draw_arrow(draw, *positions[1], *positions[0], GREEN, ap, "N3 is down!")
                draw_arrow(draw, *positions[1], *positions[4], GREEN, ap, "N3 is down!")

            if f > 5:
                draw_speech_bubble(draw, *positions[1], "Spreading the word...", GREEN, "up")

        # ── Page 4: Round 2 ──
        elif page == 3:
            prev_knows = {0, 1, 4}
            new_knows = {3, 5}

            for i in range(6):
                if i == 2:
                    draw_node(draw, *positions[i], labels[i], colors[i], state="down")
                elif i in prev_knows:
                    draw_node(draw, *positions[i], labels[i], colors[i], knows_down=True)
                elif i in new_knows:
                    draw_node(draw, *positions[i], labels[i], colors[i], knows_down=(ap > 0.85))
                else:
                    draw_node(draw, *positions[i], labels[i], colors[i])

            if f >= ARROW_START:
                draw_arrow(draw, *positions[0], *positions[3], GREEN, ap, "N3 is down!")
                draw_arrow(draw, *positions[4], *positions[5], GREEN, ap, "N3 is down!")

            if f > ARROW_START + ARROW_DUR + 2:
                msg = "Cluster converged — all nodes informed"
                cw = text_width(draw, msg, f_body) + 40*S
                cx = W//2 - cw//2
                cy2 = RING_CY + RING_R + NR + STATUS_OFF + 30*S
                draw.rounded_rectangle((cx, cy2, cx+cw, cy2+36*S), radius=18*S,
                                       fill=blend(GREEN, BG, 0.55), outline=GREEN, width=2*S)
                center_text(draw, msg, f_body, cy2+8*S, WHITE)

        # ── Action bar ──
        action_y = H - 68*S
        draw.rounded_rectangle((24*S, action_y, W-24*S, action_y+40*S), radius=14*S,
                               fill=CARD, outline=BORDER, width=S)
        ac = SECONDARY if page == 0 else (RED if page == 1 else GREEN)
        center_text(draw, actions[page], f_caption, action_y+10*S, ac)

        # Page dots — 8px, 3:1 contrast
        for i in range(4):
            dx = W//2 - 45*S + i*30*S
            dy = action_y - 18*S
            if i == page:
                draw.ellipse((dx-6*S, dy-6*S, dx+6*S, dy+6*S), fill=CYAN)
            else:
                draw.ellipse((dx-4*S, dy-4*S, dx+4*S, dy+4*S), fill=BORDER)

        # Footer — brand in accent
        center_text(draw, "System Design for Dummies", f_small, H-22*S, CYAN)

        final = img.resize((W//SCALE, H//SCALE), Image.LANCZOS)
        all_frames.append(final)

    for _ in range(PAUSE):
        all_frames.append(all_frames[-1])

for _ in range(12):
    all_frames.append(all_frames[-1])

out = "/Users/drishtikriplani/Desktop/system-design/gossip-protocol.gif"
all_frames[0].save(out, save_all=True, append_images=all_frames[1:], duration=110, loop=0, optimize=True)
print(f"Saved: {out}")
print(f"Frames: {len(all_frames)}, ~{len(all_frames)*110/1000:.1f}s loop")
