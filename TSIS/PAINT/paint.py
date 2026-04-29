# Import all necessary libraries
import pygame
import math
import sys
import platform
import subprocess

# Mac-specific: Use native file dialog instead of tkinter to avoid event loop conflicts
if platform.system() == "Darwin":  # macOS
    try:
        import applescript
    except ImportError:
        pass  # Fallback to tkinter if applescript not available

pygame.init()

# Constants, a.k.a. sizes
TOOLBAR_W = 180
CANVAS_W  = 1100
CANVAS_H  = 800
WIN_W     = TOOLBAR_W + CANVAS_W
WIN_H     = CANVAS_H
CANVAS_X  = TOOLBAR_W

# UI colours
BG       = (30,  30,  40 )
TOOLBAR  = (22,  22,  32 )
BORDER   = (55,  55,  75 )
ACCENT   = (99,  102, 241)
WHITE    = (255, 255, 255)
MUTED    = (110, 110, 135)
CANVAS_C = (255, 255, 255)

# Palette colors
PALETTE = [
    (255, 0,   0  ),   # Red
    (255, 127, 0  ),   # Orange
    (255, 255, 0  ),   # Yellow
    (0,   200, 0  ),   # Green
    (0,   0,   255),   # Blue
    (75,  0,   130),   # Indigo
    (148, 0,   211),   # Violet
]

# Names of tools
TOOLS = [
    "freehand", "line", "rectangle", "square",
    "circle", "right_triangle", "eq_triangle",
    "rhombus", "fill", "text", "eraser",
]

# A helper, shows which keys to press to access each tool
TOOL_LABELS = {
    "freehand":      "[H] Freehand",
    "line":          "[L] Line",
    "rectangle":     "[G] Rectangle",
    "square":        "[S] Square",
    "circle":        "[C] Circle",
    "right_triangle":"[R] Rt Triangle",
    "eq_triangle":   "[T] Eq Triangle",
    "rhombus":       "[P] Rhombus",
    "fill":          "[F] Fill",
    "text":          "[A] Text",
    "eraser":        "[E] Eraser",
}

# Keys and values
KEY_TO_TOOL = {
    pygame.K_h: "freehand",
    pygame.K_l: "line",
    pygame.K_g: "rectangle",
    pygame.K_s: "square",
    pygame.K_c: "circle",
    pygame.K_r: "right_triangle",
    pygame.K_t: "eq_triangle",
    pygame.K_p: "rhombus",
    pygame.K_f: "fill",
    pygame.K_a: "text",
    pygame.K_e: "eraser",
}


# Drawing Functions

def draw_eq_triangle(surf, col, p1, p2, size, fill=False):
    dx, dy = p2[0]-p1[0], p2[1]-p1[1] 
    length = math.hypot(dx, dy) or 1
    bx = p2[0] - dx / 2
    by = p2[1] - dy / 2
    perp_x = -dy / length * (math.sqrt(3)/2 * length)
    perp_y =  dx / length * (math.sqrt(3)/2 * length)
    pts = [p1,
           (int(bx + perp_x/2), int(by + perp_y/2)),
           (int(bx - perp_x/2), int(by - perp_y/2))]
    if fill: pygame.draw.polygon(surf, col, pts)
    else:    pygame.draw.polygon(surf, col, pts, max(1, size))

def draw_right_triangle(surf, col, p1, p2, size, fill=False):
    pts = [p1, (p1[0], p2[1]), p2]
    if fill: pygame.draw.polygon(surf, col, pts)
    else:    pygame.draw.polygon(surf, col, pts, max(1, size))

def draw_rhombus(surf, col, p1, p2, size, fill=False):
    cx = (p1[0]+p2[0])//2;  cy = (p1[1]+p2[1])//2
    w2 = abs(p2[0]-p1[0])//2; h2 = abs(p2[1]-p1[1])//2
    pts = [(cx,cy-h2),(cx+w2,cy),(cx,cy+h2),(cx-w2,cy)]
    if fill: pygame.draw.polygon(surf, col, pts)
    else:    pygame.draw.polygon(surf, col, pts, max(1, size))

def flood_fill(surface, x, y, new_col):
    old_col = surface.get_at((x, y))[:3]
    if old_col == new_col: return
    w, h = surface.get_size()
    stack, visited = [(x, y)], set()
    surface.lock()
    while stack:
        cx, cy = stack.pop()
        if (cx,cy) in visited: continue
        if not (0<=cx<w and 0<=cy<h): continue
        if surface.get_at((cx,cy))[:3] != old_col: continue
        surface.set_at((cx,cy), new_col)
        visited.add((cx,cy))
        stack += [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]
    surface.unlock()


# Mac-compatible save function using native dialog
def save_file(canvas):
    if platform.system() == "Darwin":  # macOS
        try:
            # Try using AppleScript for native save dialog
            script = '''
            tell application "System Events"
                set savePath to choose file name with prompt "Save canvas" default name "untitled.png"
                return POSIX path of savePath
            end tell
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip()
                # Ensure proper extension
                if not path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    path += '.png'
                pygame.image.save(canvas, path)
                return
        except Exception:
            pass  # Fall back to tkinter below
    
    # Fallback: tkinter (works but may have event loop quirks on Mac)
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)  # Help dialog appear on top
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG","*.png"),("JPEG","*.jpg"),("BMP","*.bmp")],
            title="Save canvas"
        )
        root.destroy()
        if path:
            pygame.image.save(canvas, path)
    except Exception as e:
        print(f"Save failed: {e}")


class PaintApp:
    def __init__(self):
        # Mac Retina display support: add FULLSCREEN or SCALED flags if needed
        # For windowed mode, you can add pygame.SCALED for automatic scaling:
        # self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SCALED)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        
        # Mac: Set proper window title and icon behavior
        pygame.display.set_caption("Paint")
        
        # Optional: Set window icon (Mac-compatible)
        try:
            icon = pygame.Surface((32, 32))
            icon.fill(ACCENT)
            pygame.display.set_icon(icon)
        except:
            pass

        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(CANVAS_C)

        # State
        self.tool        = "freehand"
        self.color       = (0, 0, 0)
        self.brush_size  = 4
        self.fill_shapes = False

        # Drawing
        self.drawing     = False
        self.start_pos   = None
        self.last_pos    = None
        self.prev_canvas = None

        # Text tool
        self.typing     = False
        self.text_input = ""
        self.text_pos   = None
        self.font_size  = 26
        
        # Mac font fix: Use cross-platform fonts (Segoe UI doesn't exist on macOS)
        self.text_font  = pygame.font.SysFont("Arial, Helvetica, Sans-Serif", self.font_size)

        # Fonts - Mac-compatible fallback chain
        self.font_ui    = pygame.font.SysFont("Arial, Helvetica, Sans-Serif", 14)
        self.font_bold  = pygame.font.SysFont("Arial, Helvetica, Sans-Serif", 14, bold=True)
        self.font_title = pygame.font.SysFont("Arial, Helvetica, Sans-Serif", 17, bold=True)

        self._build_rects()

    def _build_rects(self):
        self.tool_rects  = {}
        self.color_rects = {}

        x0, y0 = 8, 46
        for i, t in enumerate(TOOLS):
            self.tool_rects[t] = pygame.Rect(x0, y0 + i*36, TOOLBAR_W-16, 30)

        self._pal_top = y0 + len(TOOLS)*36 + 20
        sw = (TOOLBAR_W - 16) // 7
        for i in range(7):
            self.color_rects[i] = pygame.Rect(8 + i*sw, self._pal_top, sw-2, 28)

        self.btn_save = pygame.Rect(8, WIN_H - 46, TOOLBAR_W-16, 32)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, TOOLBAR, (0, 0, TOOLBAR_W, WIN_H))
        pygame.draw.line(self.screen, BORDER, (TOOLBAR_W-1,0),(TOOLBAR_W-1,WIN_H), 2)

        # Title
        t = self.font_title.render("Paint", True, ACCENT)
        self.screen.blit(t, (8, 10))

        # Tool buttons
        mx, my = pygame.mouse.get_pos()
        for name, rect in self.tool_rects.items():
            active  = name == self.tool
            hovered = rect.collidepoint(mx, my) and not active
            bg = ACCENT if active else ((55,55,80) if hovered else (38,38,54))
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            col = WHITE if active else MUTED
            f   = self.font_bold if active else self.font_ui
            lbl = f.render(TOOL_LABELS[name], True, col)
            self.screen.blit(lbl, (rect.x+6, rect.centery - lbl.get_height()//2))

        # Colour swatches label
        lbl = self.font_ui.render("Colours", True, MUTED)
        self.screen.blit(lbl, (8, self._pal_top - 16))

        # Swatches
        sw = (TOOLBAR_W - 16) // 7
        for i, col in enumerate(PALETTE):
            r = pygame.Rect(8 + i*sw, self._pal_top, sw-2, 28)
            self.color_rects[i] = r
            pygame.draw.rect(self.screen, col, r, border_radius=4)
            if col == self.color:
                pygame.draw.rect(self.screen, WHITE, r, 2, border_radius=4)

        # Current colour dot + brush size
        dot_y = self._pal_top + 36
        pygame.draw.rect(self.screen, self.color,
                         pygame.Rect(8, dot_y, 22, 16), border_radius=3)
        pygame.draw.rect(self.screen, BORDER,
                         pygame.Rect(8, dot_y, 22, 16), 1, border_radius=3)
        info = self.font_ui.render(f"size: {self.brush_size}", True, MUTED)
        self.screen.blit(info, (36, dot_y))

        # Keyboard hints - Mac: Show Cmd instead of Ctrl
        cmd_key = "⌘" if platform.system() == "Darwin" else "Ctrl"
        for i, h in enumerate([f"+/- : brush size", f"{cmd_key}+S : save"]):
            hs = self.font_ui.render(h, True, MUTED)
            self.screen.blit(hs, (8, WIN_H - 100 + i*18))

        # Save button
        pygame.draw.rect(self.screen, ACCENT, self.btn_save, border_radius=7)
        bs = self.font_bold.render(f"Save  {cmd_key}+S", True, WHITE)
        self.screen.blit(bs, (self.btn_save.centerx - bs.get_width()//2,
                              self.btn_save.centery - bs.get_height()//2))

    def draw_canvas(self):
        self.screen.blit(self.canvas, (CANVAS_X, 0))
        pygame.draw.rect(self.screen, BORDER,
                         (CANVAS_X-1, -1, CANVAS_W+2, CANVAS_H+2), 1)

    def _render_shape(self, surf, tool, sx, sy, ex, ey, col, bs, fill):
        if tool == "line":
            pygame.draw.line(surf,col,(sx,sy),(ex,ey),max(1,bs))
        elif tool == "rectangle":
            x0,y0 = min(sx,ex),min(sy,ey); w,h = abs(ex-sx),abs(ey-sy)
            if fill: pygame.draw.rect(surf,col,(x0,y0,w,h))
            else:    pygame.draw.rect(surf,col,(x0,y0,w,h),max(1,bs))
        elif tool == "square":
            side = min(abs(ex-sx),abs(ey-sy))
            x0 = sx if ex>=sx else sx-side
            y0 = sy if ey>=sy else sy-side
            if fill: pygame.draw.rect(surf,col,(x0,y0,side,side))
            else:    pygame.draw.rect(surf,col,(x0,y0,side,side),max(1,bs))
        elif tool == "circle":
            cx2,cy2 = (sx+ex)//2,(sy+ey)//2
            rx,ry = abs(ex-sx)//2,abs(ey-sy)//2
            if rx>0 and ry>0:
                e = pygame.Surface((rx*2,ry*2),pygame.SRCALPHA)
                if fill: pygame.draw.ellipse(e,(*col,255),(0,0,rx*2,ry*2))
                else:    pygame.draw.ellipse(e,(*col,255),(0,0,rx*2,ry*2),max(1,bs))
                surf.blit(e,(cx2-rx,cy2-ry))
        elif tool == "right_triangle":
            draw_right_triangle(surf,col,(sx,sy),(ex,ey),bs,fill)
        elif tool == "eq_triangle":
            draw_eq_triangle(surf,col,(sx,sy),(ex,ey),bs,fill)
        elif tool == "rhombus":
            draw_rhombus(surf,col,(sx,sy),(ex,ey),bs,fill)

    def draw_text_overlay(self):
        """Draw the text being typed with a blinking cursor"""
        if not self.typing or self.text_pos is None:
            return
        
        # Render the current text
        text_surface = self.text_font.render(self.text_input, True, self.color)
        tx, ty = self.text_pos
        
        # Draw text on screen (not on canvas yet)
        self.screen.blit(text_surface, (CANVAS_X + tx, ty))
        
        # Draw blinking cursor
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = CANVAS_X + tx + text_surface.get_width()
            cursor_y = ty
            cursor_height = self.font_size
            pygame.draw.line(self.screen, self.color, 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + cursor_height), 2)

    def _to_canvas(self, sx, sy): return sx - CANVAS_X, sy
    def _in_canvas(self, sx, sy): return sx >= CANVAS_X and 0 <= sy < CANVAS_H

    def _commit_text(self):
        """Commit the typed text to the canvas"""
        if self.text_input and self.text_pos:
            text_surface = self.text_font.render(self.text_input, True, self.color)
            self.canvas.blit(text_surface, self.text_pos)
        self.typing = False
        self.text_input = ""
        self.text_pos = None

    def _set_cursor(self):
        mx, my = pygame.mouse.get_pos()
        if mx >= CANVAS_X:
            if self.tool == "text":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()

        if event.type == pygame.QUIT: sys.exit()

        # KEYBOARD
        if event.type == pygame.KEYDOWN:
            if self.typing:
                if event.key == pygame.K_RETURN:   # Enter - commit text
                    self._commit_text()
                    return
                elif event.key == pygame.K_ESCAPE:  # Escape - cancel
                    self.typing = False
                    self.text_input = ""
                    self.text_pos = None
                    return
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                    return
                else:
                    # Add typed character
                    if event.unicode:
                        self.text_input += event.unicode
                    return

            mods = pygame.key.get_mods()
            # Mac fix: Support both Ctrl AND Cmd (META) for save shortcut
            ctrl_or_cmd = bool(mods & (pygame.KMOD_CTRL | pygame.KMOD_META))

            # Cmd/Ctrl+S — save (works on both Mac and Windows/Linux)
            if event.key == pygame.K_s and ctrl_or_cmd:
                save_file(self.canvas); return

            # +/- — brush size
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                self.brush_size = min(50, self.brush_size + 2); return
            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.brush_size = max(1, self.brush_size - 2); return

            # Tool hotkeys (only when not holding modifier)
            if not ctrl_or_cmd and event.key in KEY_TO_TOOL:
                self.tool = KEY_TO_TOOL[event.key]; return

        # MOUSE DOWN
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # If clicking on canvas while typing, commit text first
            if self.typing and self._in_canvas(mx, my):
                self._commit_text()
            
            # Tool buttons
            for name, rect in self.tool_rects.items():
                if rect.collidepoint(mx, my):
                    if self.typing: self._commit_text()
                    self.tool = name; return
            # Colour swatches
            for i in range(7):
                if self.color_rects[i].collidepoint(mx, my):
                    if self.typing: self._commit_text()
                    self.color = PALETTE[i]; return
            # Save button
            if self.btn_save.collidepoint(mx, my):
                if self.typing: self._commit_text()
                save_file(self.canvas); return
            # Canvas
            if not self._in_canvas(mx, my): return
            cx, cy = self._to_canvas(mx, my)
            if self.tool == "fill":
                flood_fill(self.canvas, cx, cy, self.color); return
            if self.tool == "text":
                if self.typing: self._commit_text()
                self.text_pos = (cx,cy)
                self.text_input = ""
                self.typing = True
                return
            # Eraser and freehand
            if self.tool in ("eraser", "freehand"):
                self.drawing  = True
                self.last_pos = (cx, cy)
            else:
                # Shape tools need a clean snapshot to draw preview on
                self.drawing     = True
                self.start_pos   = (cx, cy)
                self.last_pos    = (cx, cy)
                self.prev_canvas = self.canvas.copy()

        # MOUSE MOTION
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if not self._in_canvas(mx, my) or not self.drawing: return
            cx, cy = self._to_canvas(mx, my)
            if self.tool == "freehand":
                pygame.draw.line(self.canvas, self.color,
                                 self.last_pos, (cx, cy), max(1, self.brush_size))
                pygame.draw.circle(self.canvas, self.color,
                                   (cx, cy), max(1, self.brush_size) // 2)
            elif self.tool == "eraser":
                pygame.draw.circle(self.canvas, CANVAS_C,
                                   (cx, cy), max(2, self.brush_size))
            self.last_pos = (cx, cy)

        # MOUSE UP
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.drawing and self.tool not in ("eraser", "freehand"):
                cx, cy = self._to_canvas(mx, my)
                # Restore clean snapshot, then draw final shape
                if self.prev_canvas:
                    self.canvas.blit(self.prev_canvas, (0, 0))
                self._render_shape(self.canvas, self.tool,
                                   *self.start_pos, cx, cy,
                                   self.color, self.brush_size, self.fill_shapes)
            self.drawing = False; self.start_pos = None; self.prev_canvas = None

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.screen.fill(BG)
            
            # Always draw the base canvas
            self.screen.blit(self.canvas, (CANVAS_X, 0))
            
            self.draw_toolbar()

            mx, my = pygame.mouse.get_pos()
            
            # For shape tools, draw preview directly in run loop
            if self.drawing and self.tool not in ("freehand","eraser","fill","text"):
                if self.prev_canvas:
                    # Restore canvas for preview
                    temp_canvas = self.prev_canvas.copy()
                    ex, ey = self._to_canvas(mx, my)
                    self._render_shape(temp_canvas, self.tool,
                                       *self.start_pos, ex, ey,
                                       self.color, self.brush_size, self.fill_shapes)
                    self.screen.blit(temp_canvas, (CANVAS_X, 0))

            # Draw text overlay if typing
            if self.typing:
                self.draw_text_overlay()

            if self.tool == "eraser" and mx >= CANVAS_X:
                pygame.draw.circle(self.screen,(180,180,180),(mx,my),max(2,self.brush_size),1)

            self._set_cursor()
            pygame.display.flip()
            clock.tick(120)


if __name__ == "__main__":
    # Mac-specific: Ensure pygame initializes properly with the display
    if platform.system() == "Darwin":
        # Optional: Enable Retina scaling support
        # import os
        # os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        pass
    
    try:
        PaintApp().run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()