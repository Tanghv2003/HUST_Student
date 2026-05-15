"""Design tokens aligned with Quizlet (navy primary, warm neutrals, soft shadows)."""

# ── Base ─────────────────────────────────────────────────────────
PAGE_BG = "#F6F7FB"
SURFACE = "#FFFFFF"

TEXT_PRIMARY = "#2E3856"
TEXT_SECONDARY = "#586380"
TEXT_MUTED = "#939BB4"

# ── Brand (Quizlet blue family) ───────────────────────────────────
PRIMARY = "#4257B2"
PRIMARY_HOVER = "#35448F"
PRIMARY_LIGHT = "#E8EDF8"
PRIMARY_TINT = "#EDF2FF"
PRIMARY_DISABLED = "#B8C4E8"

# ── Lines & depth ────────────────────────────────────────────────
BORDER = "#D9DCE2"
BORDER_LIGHT = "#EEF1F5"
DIVIDER = "#EDEFF4"

SHADOW_MODAL = "0 12px 48px rgba(46, 56, 86, 0.18)"
SHADOW_CARD = "0 2px 8px rgba(46, 56, 86, 0.08)"
SHADOW_CARD_HOVER = "0 6px 20px rgba(46, 56, 86, 0.12)"

RADIUS_SM = "10px"
RADIUS_MD = "14px"
RADIUS_LG = "18px"
RADIUS_XL = "24px"
RADIUS_PILL = "999px"

OVERLAY_SCRIM = "rgba(30, 40, 60, 0.55)"

# Khoảng cách modal với mép trên/dưới viewport (không tràn màn hình)
MODAL_OVERLAY_PADDING = "1.75rem 1.25rem"
MODAL_CONTENT_MAX_HEIGHT = "calc(100dvh - 3.5rem)"

# ── Feedback ─────────────────────────────────────────────────────
SUCCESS = "#23B26D"
SUCCESS_BG = "#E8F8F0"
DANGER = "#E64646"
DANGER_BG = "#FDECEC"
WARN = "#FF9B37"

# ── Marketing / CTA ─────────────────────────────────────────────
UPGRADE_YELLOW = "#FFCD1F"
UPGRADE_TEXT = "#2E3856"

# ── Study surfaces (learn + flashcards) ─────────────────────────
LEARN_CARD_BG = "linear-gradient(180deg, #F7F9FF 0%, #EDF2FF 100%)"
LEARN_CARD_BORDER = "#C5D0EF"
LEARN_LABEL = PRIMARY

QUESTION_BOX_BG = "#F7F9FF"
QUESTION_BOX_BORDER = "#C5D0EF"
QUESTION_BOX_ALT_BG = "#FFFBF5"
QUESTION_BOX_ALT_BORDER = "#F5E6D3"
