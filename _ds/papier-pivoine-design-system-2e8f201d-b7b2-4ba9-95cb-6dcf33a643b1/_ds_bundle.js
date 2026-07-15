/* @ds-bundle: {"format":3,"namespace":"PapierPivoineDesignSystem_2e8f20","components":[{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Divider","sourcePath":"components/core/Divider.jsx"},{"name":"Tag","sourcePath":"components/core/Tag.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"TextField","sourcePath":"components/forms/TextField.jsx"},{"name":"Textarea","sourcePath":"components/forms/Textarea.jsx"},{"name":"Card","sourcePath":"components/surfaces/Card.jsx"},{"name":"LetterBlock","sourcePath":"components/surfaces/LetterBlock.jsx"},{"name":"PivoineBadge","sourcePath":"components/surfaces/PivoineBadge.jsx"}],"sourceHashes":{"components/core/Button.jsx":"f87cb18edfde","components/core/Divider.jsx":"3c661a476e24","components/core/Tag.jsx":"7fcc7650a0c5","components/forms/Checkbox.jsx":"ab4ab0f6cbeb","components/forms/TextField.jsx":"62af91c3955b","components/forms/Textarea.jsx":"810a7277b6d4","components/surfaces/Card.jsx":"90762a01df07","components/surfaces/LetterBlock.jsx":"fdf7c921a256","components/surfaces/PivoineBadge.jsx":"9c8048f453c1","ui_kits/journal/Pages.jsx":"6f75950d30b5","ui_kits/journal/Sheet.jsx":"ea6152b78e3a","ui_kits/journal/WritingPages.jsx":"1f3fe062fc3b","ui_kits/website/BooksPage.jsx":"c3676b4c32b6","ui_kits/website/Footer.jsx":"35ef409e5a67","ui_kits/website/Home.jsx":"252d101773e8","ui_kits/website/Illustration.jsx":"39d44d325a91","ui_kits/website/LetterPage.jsx":"4d2f95495214","ui_kits/website/ProductPage.jsx":"3ffa2e6af520","ui_kits/website/SiteHeader.jsx":"a9dd53f97b5a"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.PapierPivoineDesignSystem_2e8f20 = window.PapierPivoineDesignSystem_2e8f20 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Button
 * Soft, calm call-to-action. Warm tints, gentle press settle, no bounce.
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  fullWidth = false,
  iconStart = null,
  iconEnd = null,
  type = 'button',
  onClick,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);
  const sizes = {
    sm: {
      padding: '8px 16px',
      fontSize: 'var(--text-sm)'
    },
    md: {
      padding: '12px 24px',
      fontSize: 'var(--text-base)'
    },
    lg: {
      padding: '15px 32px',
      fontSize: 'var(--text-md)'
    }
  };
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    width: fullWidth ? '100%' : 'auto',
    fontFamily: 'var(--font-body)',
    fontWeight: 'var(--weight-medium)',
    letterSpacing: '0.01em',
    lineHeight: 1.2,
    borderRadius: 'var(--radius-pill)',
    border: '1px solid transparent',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.45 : 1,
    transition: 'background var(--dur-base) var(--ease-soft), border-color var(--dur-base) var(--ease-soft), color var(--dur-base) var(--ease-soft), transform var(--dur-fast) var(--ease-soft)',
    transform: active && !disabled ? 'translateY(1px)' : 'translateY(0)',
    ...sizes[size]
  };
  const variants = {
    primary: {
      background: hover && !disabled ? 'var(--rose-deep)' : 'var(--rose)',
      color: 'var(--text-on-accent)',
      boxShadow: 'var(--shadow-xs)'
    },
    secondary: {
      background: hover && !disabled ? 'var(--olive-soft)' : 'transparent',
      color: 'var(--deep-olive)',
      borderColor: 'var(--deep-olive)'
    },
    soft: {
      background: hover && !disabled ? 'var(--blush-deep)' : 'var(--blush)',
      color: 'var(--deep-olive)'
    },
    ghost: {
      background: 'transparent',
      color: hover && !disabled ? 'var(--rose-deep)' : 'var(--rose)'
    }
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
    style: {
      ...base,
      ...variants[variant],
      ...style
    }
  }, rest), iconStart, children, iconEnd);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Divider.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Divider
 * A hairline rule, optionally with a small centred ornament. Sage by default.
 */
function Divider({
  ornament = false,
  tone = 'sage',
  spacing = 'var(--space-6)',
  style = {},
  ...rest
}) {
  const color = tone === 'rose' ? 'var(--border-soft)' : tone === 'faint' ? 'var(--border-faint)' : 'var(--sage)';
  if (ornament) {
    return /*#__PURE__*/React.createElement("div", _extends({
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        margin: `${spacing} 0`,
        ...style
      }
    }, rest), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        height: '1px',
        background: color,
        opacity: 0.7
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        color: 'var(--rose)',
        fontSize: 'var(--text-sm)',
        lineHeight: 1
      }
    }, "\u2726"), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        height: '1px',
        background: color,
        opacity: 0.7
      }
    }));
  }
  return /*#__PURE__*/React.createElement("hr", _extends({
    style: {
      border: 'none',
      height: '1px',
      background: color,
      opacity: 0.7,
      margin: `${spacing} 0`,
      ...style
    }
  }, rest));
}
Object.assign(__ds_scope, { Divider });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Divider.jsx", error: String((e && e.message) || e) }); }

// components/core/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Tag
 * Quiet label / pill for themes, categories, status. Soft tinted fills.
 */
function Tag({
  children,
  tone = 'sage',
  style = {},
  ...rest
}) {
  const tones = {
    sage: {
      background: 'var(--sage-soft)',
      color: 'var(--deep-olive)'
    },
    rose: {
      background: 'var(--blush)',
      color: 'var(--rose-deep)'
    },
    olive: {
      background: 'var(--olive-soft)',
      color: 'var(--deep-olive)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--text-muted)',
      border: '1px solid var(--border-soft)'
    }
  };
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      padding: '5px 13px',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      fontWeight: 'var(--weight-medium)',
      letterSpacing: '0.04em',
      lineHeight: 1.4,
      borderRadius: 'var(--radius-pill)',
      ...tones[tone],
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tag.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Checkbox
 * A soft, rounded check. Sage when on. Gentle, never a hard toggle.
 */
function Checkbox({
  label,
  checked = false,
  onChange,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const inputId = id || React.useId();
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '11px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-base)',
      color: 'var(--text-body)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    type: "checkbox",
    checked: checked,
    onChange: onChange,
    disabled: disabled,
    style: {
      position: 'absolute',
      opacity: 0,
      width: 0,
      height: 0
    }
  }, rest)), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      width: '22px',
      height: '22px',
      flex: 'none',
      borderRadius: 'var(--radius-xs)',
      border: `1px solid ${checked ? 'var(--deep-olive)' : 'var(--border-soft)'}`,
      background: checked ? 'var(--sage)' : 'var(--paper)',
      boxShadow: checked ? 'none' : 'var(--shadow-inset)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'all var(--dur-base) var(--ease-soft)'
    }
  }, checked && /*#__PURE__*/React.createElement("svg", {
    width: "13",
    height: "13",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "var(--deep-olive)",
    strokeWidth: "3",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("polyline", {
    points: "20 6 9 17 4 12"
  }))), label && /*#__PURE__*/React.createElement("span", null, label));
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/TextField.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — TextField
 * A single-line input with a calm label. Soft inset, warm focus ring.
 */
function TextField({
  label,
  hint,
  value,
  onChange,
  placeholder = '',
  type = 'text',
  id,
  disabled = false,
  style = {},
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || React.useId();
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '7px',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--text-muted)'
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    type: type,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-base)',
      color: 'var(--text-body)',
      background: disabled ? 'var(--blush)' : 'var(--paper)',
      padding: '12px 15px',
      borderRadius: 'var(--radius-sm)',
      border: `1px solid ${focus ? 'var(--rose)' : 'var(--border-soft)'}`,
      boxShadow: focus ? '0 0 0 3px rgba(196,122,120,0.15)' : 'var(--shadow-inset)',
      outline: 'none',
      transition: 'border-color var(--dur-base) var(--ease-soft), box-shadow var(--dur-base) var(--ease-soft)'
    }
  }, rest)), hint && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-faint)'
    }
  }, hint));
}
Object.assign(__ds_scope, { TextField });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/TextField.jsx", error: String((e && e.message) || e) }); }

// components/forms/Textarea.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Textarea
 * The writing surface. Generous line-height, ruled-paper option, unhurried.
 */
function Textarea({
  label,
  value,
  onChange,
  placeholder = '',
  rows = 5,
  ruled = false,
  id,
  style = {},
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const inputId = id || React.useId();
  const lineHeight = 34;
  const ruledBg = ruled ? {
    backgroundImage: 'repeating-linear-gradient(to bottom, transparent, transparent ' + (lineHeight - 1) + 'px, var(--border-faint) ' + (lineHeight - 1) + 'px, var(--border-faint) ' + lineHeight + 'px)',
    backgroundAttachment: 'local',
    lineHeight: lineHeight + 'px',
    padding: '8px 16px'
  } : {
    lineHeight: 'var(--leading-relaxed)',
    padding: '14px 16px'
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '7px',
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--text-muted)'
    }
  }, label), /*#__PURE__*/React.createElement("textarea", _extends({
    id: inputId,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    rows: rows,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-md)',
      color: 'var(--text-body)',
      background: 'var(--paper)',
      borderRadius: 'var(--radius-md)',
      border: `1px solid ${focus ? 'var(--rose)' : 'var(--border-soft)'}`,
      boxShadow: focus ? '0 0 0 3px rgba(196,122,120,0.13)' : 'var(--shadow-inset)',
      outline: 'none',
      resize: 'vertical',
      transition: 'border-color var(--dur-base) var(--ease-soft), box-shadow var(--dur-base) var(--ease-soft)',
      ...ruledBg
    }
  }, rest)));
}
Object.assign(__ds_scope, { Textarea });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Textarea.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — Card
 * A quiet surface: warm white, very soft shadow, gentle radius.
 * Optional hover lift for clickable product cards.
 */
function Card({
  children,
  tone = 'paper',
  interactive = false,
  padded = true,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const fills = {
    paper: 'var(--paper)',
    blush: 'var(--blush)',
    warm: 'var(--paper-warm)'
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => interactive && setHover(true),
    onMouseLeave: () => interactive && setHover(false),
    style: {
      background: fills[tone] || fills.paper,
      border: '1px solid var(--border-faint)',
      borderRadius: 'var(--radius-md)',
      padding: padded ? 'var(--pad-card)' : 0,
      boxShadow: interactive && hover ? 'var(--shadow-md)' : 'var(--shadow-sm)',
      transform: interactive && hover ? 'translateY(-2px)' : 'translateY(0)',
      transition: 'box-shadow var(--dur-base) var(--ease-soft), transform var(--dur-base) var(--ease-soft)',
      cursor: interactive ? 'pointer' : 'default',
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Card.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/LetterBlock.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Papier Pivoine — LetterBlock
 * A letter in the brand's voice. Narrow measure, relaxed reading,
 * signed in display type. Use for welcomes, reassurances, closings.
 */
function LetterBlock({
  children,
  signature = 'Camélia Nguyen',
  align = 'left',
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      maxWidth: 'var(--measure-narrow)',
      marginLeft: align === 'center' ? 'auto' : 0,
      marginRight: align === 'center' ? 'auto' : 0,
      textAlign: align,
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-md)',
      lineHeight: 'var(--leading-relaxed)',
      color: 'var(--text-body)',
      ...style
    }
  }, rest), children, signature && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'var(--space-5)',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-base)',
      letterSpacing: '0.04em',
      color: 'var(--deep-olive)'
    }
  }, signature));
}
Object.assign(__ds_scope, { LetterBlock });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/LetterBlock.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/PivoineBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const PERMISSIONS = [{
  l: 'P',
  word: 'Poser',
  gloss: 'déposer ce que tu portes'
}, {
  l: 'I',
  word: 'Intimité',
  gloss: "rien qu'à toi"
}, {
  l: 'V',
  word: 'Vérité',
  gloss: 'sans te juger'
}, {
  l: 'O',
  word: 'Observer',
  gloss: 'les petites choses'
}, {
  l: 'I',
  word: 'Imperfection',
  gloss: 'rien à réussir'
}, {
  l: 'N',
  word: 'Nature',
  gloss: 'laisser entrer la saison'
}, {
  l: 'E',
  word: 'Émerveillement',
  gloss: 'un peu de douceur'
}];

/**
 * Papier Pivoine — PivoineBadge
 * The seven gentle permissions. "strip" shows the acronym letters;
 * "list" shows each permission with its plain-word gloss.
 */
function PivoineBadge({
  variant = 'strip',
  active = -1,
  style = {},
  ...rest
}) {
  if (variant === 'list') {
    return /*#__PURE__*/React.createElement("div", _extends({
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        ...style
      }
    }, rest), PERMISSIONS.map((p, i) => /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        display: 'flex',
        alignItems: 'baseline',
        gap: '14px'
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-display)',
        fontSize: 'var(--text-xl)',
        color: 'var(--rose)',
        width: '28px',
        flex: 'none',
        lineHeight: 1
      }
    }, p.l), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-body)',
        fontWeight: 'var(--weight-medium)',
        color: 'var(--deep-olive)',
        fontSize: 'var(--text-md)'
      }
    }, p.word), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-body)',
        color: 'var(--text-muted)',
        fontSize: 'var(--text-sm)',
        marginLeft: '8px'
      }
    }, "\u2014 ", p.gloss)))));
  }
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'inline-flex',
      gap: '10px',
      ...style
    }
  }, rest), PERMISSIONS.map((p, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    title: p.word,
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      width: '40px',
      height: '40px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 'var(--radius-pill)',
      color: i === active ? 'var(--text-on-accent)' : 'var(--deep-olive)',
      background: i === active ? 'var(--rose)' : 'var(--blush)',
      transition: 'all var(--dur-base) var(--ease-soft)'
    }
  }, p.l)));
}
Object.assign(__ds_scope, { PivoineBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/PivoineBadge.jsx", error: String((e && e.message) || e) }); }

// ui_kits/journal/Pages.jsx
try { (() => {
/* global React, Sheet */
// Papier Pivoine — the journal interior pages. Each is an A4 sheet.

function CoverPage() {
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "Un moment \xE0 toi"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 28
    }
  }, "Papier Pivoine"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-3xl)',
      lineHeight: 1.15,
      margin: '0 0 22px',
      color: 'var(--deep-olive)'
    }
  }, "Quand ma t\xEAte", /*#__PURE__*/React.createElement("br", null), "est pleine"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 44,
      height: 1,
      background: 'var(--sage)',
      margin: '0 0 22px'
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-body)',
      fontStyle: 'italic',
      color: 'var(--rose)',
      fontSize: 'var(--text-md)',
      margin: '0 0 40px',
      maxWidth: '24ch'
    }
  }, "Un carnet d'\xE9criture pour apaiser un esprit qui pense trop."), /*#__PURE__*/React.createElement("p", {
    className: "pp-eyebrow",
    style: {
      color: 'var(--text-faint)'
    }
  }, "Pour femmes hypersensibles et introverties")));
}
window.CoverPage = CoverPage;
function WelcomePage() {
  const {
    LetterBlock
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "1"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 32
    }
  }, "Avant de commencer"), /*#__PURE__*/React.createElement(LetterBlock, {
    style: {
      maxWidth: '100%',
      fontSize: 'var(--text-md)'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 0
    }
  }, "Bonjour, et bienvenue. Je suis contente que tu sois l\xE0."), /*#__PURE__*/React.createElement("p", null, "Tu n'as rien \xE0 faire ni \xE0 r\xE9parer ce soir. C'est seulement un endroit calme pour d\xE9poser ce que tu portes."), /*#__PURE__*/React.createElement("p", null, "\xC9cris ce qui vient, dans l'ordre que tu veux, ou pas d'ordre du tout. Il n'y a pas de bonne r\xE9ponse ici, seulement la tienne."), /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 0
    }
  }, "Prends ton temps. Rien ne presse.")));
}
window.WelcomePage = WelcomePage;
function MethodPage() {
  const {
    PivoineBadge
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "2"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 12
    }
  }, "La m\xE9thode pivoine"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-xl)',
      margin: '0 0 10px'
    }
  }, "Ce que la page te permet"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-body)',
      color: 'var(--text-muted)',
      fontSize: 'var(--text-sm)',
      lineHeight: 1.7,
      margin: '0 0 30px',
      maxWidth: '38ch'
    }
  }, "Sept petites permissions. Tu n'as pas \xE0 toutes les suivre, ni dans l'ordre. Elles sont l\xE0, simplement, quand tu en as besoin."), /*#__PURE__*/React.createElement(PivoineBadge, {
    variant: "list"
  }));
}
window.MethodPage = MethodPage;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/journal/Pages.jsx", error: String((e && e.message) || e) }); }

// ui_kits/journal/Sheet.jsx
try { (() => {
/* global React */
// Papier Pivoine — an A4 "paper sheet" for the printable journal interior.
// Light on ink, generous margins, warm paper.
function Sheet({
  children,
  footer
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: 480,
      minHeight: 679,
      background: 'var(--paper)',
      boxShadow: 'var(--shadow-lg)',
      borderRadius: 2,
      padding: '52px 56px',
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, children), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 28,
      textAlign: 'center',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-faint)',
      letterSpacing: '0.08em'
    }
  }, footer || 'Papier Pivoine'));
}
window.Sheet = Sheet;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/journal/Sheet.jsx", error: String((e && e.message) || e) }); }

// ui_kits/journal/WritingPages.jsx
try { (() => {
/* global React, Sheet */
// Papier Pivoine — the writing pages (the heart of the printable).

// A faint ruled writing area (for the printable, lines are printed, not interactive).
function RuledLines({
  count = 9,
  gap = 30
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6
    }
  }, Array.from({
    length: count
  }).map((_, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      height: gap,
      borderBottom: '1px solid var(--border-faint)'
    }
  })));
}
function WritingPage() {
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 10
    }
  }, "Ce soir"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-lg)',
      margin: '0 0 6px',
      color: 'var(--deep-olive)'
    }
  }, "Qu'est-ce que tu portes, l\xE0, maintenant ?"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-body)',
      fontStyle: 'italic',
      color: 'var(--text-faint)',
      fontSize: 'var(--text-sm)',
      margin: '0 0 14px'
    }
  }, "\xC9cris seulement ce qui te semble vrai, et laisse le reste."), /*#__PURE__*/React.createElement(RuledLines, {
    count: 11
  }));
}
window.WritingPage = WritingPage;
function NoticePage() {
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 10
    }
  }, "Avant de fermer"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-lg)',
      margin: '0 0 6px',
      color: 'var(--deep-olive)'
    }
  }, "Qu'est-ce qui s'est apais\xE9, m\xEAme un peu ?"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-body)',
      fontStyle: 'italic',
      color: 'var(--text-faint)',
      fontSize: 'var(--text-sm)',
      margin: '0 0 20px'
    }
  }, "Rien \xE0 trouver de pr\xE9cis. Juste ce que tu remarques."), /*#__PURE__*/React.createElement(RuledLines, {
    count: 5
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 28
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 10
    }
  }, "Une petite chose belle aujourd'hui"), /*#__PURE__*/React.createElement(RuledLines, {
    count: 2
  })));
}
window.NoticePage = NoticePage;
function ClosingPage() {
  const {
    LetterBlock,
    Divider
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement(Sheet, {
    footer: "Un moment \xE0 toi"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(Divider, {
    ornament: true,
    spacing: "0 0 28px"
  }), /*#__PURE__*/React.createElement(LetterBlock, {
    align: "center",
    style: {
      maxWidth: '100%'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 0
    }
  }, "Tu peux refermer quand tu veux. Ce que tu as \xE9crit ne s'en va pas."), /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 0
    }
  }, "Et cet endroit non plus. Il sera l\xE0 demain, le m\xEAme que ce soir."))));
}
window.ClosingPage = ClosingPage;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/journal/WritingPages.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/BooksPage.jsx
try { (() => {
/* global React, Illustration */
// Papier Pivoine — the activity-book series (themed catalog).
function BooksPage({
  onNav
}) {
  const {
    Card,
    Tag,
    Button
  } = window.PapierPivoineDesignSystem_2e8f20;
  const themes = [{
    t: 'Jardin',
    tone: 'sage',
    d: 'Fleurs, feuillages, le calme d\'un jardin au matin.'
  }, {
    t: 'Bouquet floral',
    tone: 'rose',
    d: 'Pivoines, roses et pétales à colorier doucement.'
  }, {
    t: 'Récolte d\'automne',
    tone: 'warm',
    d: 'Lumière dorée, courges, feuilles qui tombent.'
  }, {
    t: 'Forêt tropicale',
    tone: 'sage',
    d: 'Verts profonds, fougères, pluie tiède.'
  }, {
    t: 'Océan',
    tone: 'blush',
    d: 'Vagues lentes, coquillages, bleu apaisant.'
  }, {
    t: 'Fêtes de Noël',
    tone: 'rose',
    d: 'Branches de sapin, douceur de décembre.'
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1180,
      margin: '0 auto',
      padding: '64px 48px 88px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      marginBottom: 48
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 16
    }
  }, "Les cahiers"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-3xl)',
      margin: '0 0 16px'
    }
  }, "Une s\xE9rie, au fil des saisons"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-md)',
      color: 'var(--text-muted)',
      maxWidth: '46ch',
      margin: '0 auto',
      lineHeight: 'var(--leading-relaxed)'
    }
  }, "Colorier, \xE9crire, observer, jouer. Chaque cahier a son th\xE8me. La m\xEAme m\xE9thode, le m\xEAme calme, \xE0 chaque fois.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: 28
    }
  }, themes.map(th => /*#__PURE__*/React.createElement(Card, {
    key: th.t,
    interactive: true,
    padded: false,
    style: {
      overflow: 'hidden'
    },
    onClick: () => onNav('journal')
  }, /*#__PURE__*/React.createElement(Illustration, {
    label: th.t,
    height: 170,
    radius: "0",
    tone: th.tone
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-5)'
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: 'var(--text-lg)',
      margin: '0 0 8px'
    }
  }, th.t), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-sm)',
      margin: 0,
      lineHeight: 1.6
    }
  }, th.d))))));
}
window.BooksPage = BooksPage;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/BooksPage.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Footer.jsx
try { (() => {
/* global React, Illustration */
// Papier Pivoine — freebie band + footer.
function FreebieBand({
  onNav
}) {
  const {
    Button
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'var(--blush)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 760,
      margin: '0 auto',
      padding: '76px 48px',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-2xl)',
      margin: '0 0 16px'
    }
  }, "Commence par un cadeau"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-md)',
      color: 'var(--text-muted)',
      lineHeight: 'var(--leading-relaxed)',
      maxWidth: '40ch',
      margin: '0 auto 28px'
    }
  }, "Une premi\xE8re le\xE7on de la m\xE9thode pivoine et quelques pages \xE0 imprimer. Pour voir si \xE7a te fait du bien, avant tout le reste."), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    onClick: () => onNav('letter')
  }, "Recevoir le cadeau")));
}
window.FreebieBand = FreebieBand;
function SiteFooter() {
  const {
    Divider
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      background: 'var(--paper-warm)',
      borderTop: '1px solid var(--border-faint)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1180,
      margin: '0 auto',
      padding: '56px 48px 40px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      flexWrap: 'wrap',
      gap: 32
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      color: 'var(--deep-olive)',
      letterSpacing: '0.06em',
      marginBottom: 8
    }
  }, "Papier Pivoine"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontStyle: 'italic',
      color: 'var(--rose)',
      margin: 0,
      fontSize: 'var(--text-sm)'
    }
  }, "Un moment \xE0 toi.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 56
    }
  }, /*#__PURE__*/React.createElement(FootCol, {
    title: "La marque",
    items: ['Le carnet', 'Les cahiers', 'La méthode']
  }), /*#__PURE__*/React.createElement(FootCol, {
    title: "Rester en lien",
    items: ['La lettre', 'Pinterest']
  }))), /*#__PURE__*/React.createElement(Divider, {
    tone: "faint",
    spacing: "36px"
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-faint)',
      margin: 0,
      maxWidth: '70ch',
      lineHeight: 1.6
    }
  }, "Ce que tu trouves ici est une pratique douce, pas un soin. Ce n'est pas un substitut \xE0 un accompagnement professionnel. Si tu traverses une p\xE9riode difficile, parles-en \xE0 un professionnel de sant\xE9.")));
}
function FootCol({
  title,
  items
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 14
    }
  }, title), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: 'none',
      padding: 0,
      margin: 0,
      display: 'flex',
      flexDirection: 'column',
      gap: 9
    }
  }, items.map(i => /*#__PURE__*/React.createElement("li", {
    key: i
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      fontSize: 'var(--text-sm)',
      color: 'var(--text-muted)'
    }
  }, i)))));
}
window.SiteFooter = SiteFooter;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Footer.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Home.jsx
try { (() => {
/* global React, Illustration, PapierPivoineDesignSystem_2e8f20 */
// Papier Pivoine — homepage. Leads with the feeling, never the argument.
function Home({
  onNav
}) {
  const {
    Button,
    Divider,
    PivoineBadge,
    Card,
    Tag
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("section", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1.05fr 0.95fr',
      gap: '64px',
      alignItems: 'center',
      padding: '88px 48px 72px',
      maxWidth: 1180,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 20
    }
  }, "Un moment \xE0 toi"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-3xl)',
      lineHeight: 1.12,
      margin: '0 0 24px'
    }
  }, "Un endroit calme pour d\xE9poser ce que tu portes."), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-lg)',
      color: 'var(--text-muted)',
      lineHeight: 'var(--leading-relaxed)',
      maxWidth: '46ch',
      margin: '0 0 36px'
    }
  }, "Des carnets et des cahiers \xE0 imprimer, pens\xE9s pour les soirs o\xF9 la t\xEAte est pleine. Rien \xE0 r\xE9ussir, rien \xE0 r\xE9parer. Juste un moment, loin de l'\xE9cran."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: '14px',
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    onClick: () => onNav('letter')
  }, "Recevoir la lettre"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "lg",
    onClick: () => onNav('journal')
  }, "Voir le carnet"))), /*#__PURE__*/React.createElement(Illustration, {
    label: "Pivoine \xE0 l'aquarelle",
    height: 380,
    radius: "var(--radius-lg)"
  })), /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'var(--paper)',
      borderTop: '1px solid var(--border-faint)',
      borderBottom: '1px solid var(--border-faint)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1180,
      margin: '0 auto',
      padding: '72px 48px',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 16
    }
  }, "La m\xE9thode pivoine"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-xl)',
      color: 'var(--deep-olive)',
      letterSpacing: '0.04em',
      maxWidth: '24ch',
      margin: '0 auto 36px',
      lineHeight: 1.4
    }
  }, "Sept petites permissions. Jamais une liste \xE0 cocher."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(PivoineBadge, {
    variant: "strip"
  })))), /*#__PURE__*/React.createElement("section", {
    style: {
      maxWidth: 1180,
      margin: '0 auto',
      padding: '80px 48px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '36px'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    interactive: true,
    padded: false,
    style: {
      overflow: 'hidden'
    },
    onClick: () => onNav('journal')
  }, /*#__PURE__*/React.createElement(Illustration, {
    label: "Couverture du carnet",
    height: 220,
    radius: "0",
    tone: "warm"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement(Tag, {
    tone: "rose",
    style: {
      marginBottom: 12
    }
  }, "Le carnet"), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: 'var(--text-xl)',
      margin: '0 0 10px'
    }
  }, "Quand ma t\xEAte est pleine"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-base)',
      margin: 0
    }
  }, "Un carnet d'\xE9criture pour apaiser un esprit qui pense trop. \xC0 imprimer, \xE0 remplir \xE0 la main, \xE0 ton rythme."))), /*#__PURE__*/React.createElement(Card, {
    interactive: true,
    padded: false,
    style: {
      overflow: 'hidden'
    },
    onClick: () => onNav('books')
  }, /*#__PURE__*/React.createElement(Illustration, {
    label: "Cahiers d'activit\xE9s",
    height: 220,
    radius: "0",
    tone: "sage"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-6)'
    }
  }, /*#__PURE__*/React.createElement(Tag, {
    tone: "sage",
    style: {
      marginBottom: 12
    }
  }, "Les cahiers"), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: 'var(--text-xl)',
      margin: '0 0 10px'
    }
  }, "Les cahiers d'activit\xE9s"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-base)',
      margin: 0
    }
  }, "Colorier, \xE9crire, observer. Une s\xE9rie douce, au fil des saisons. Le m\xEAme calme, une autre porte."))))), /*#__PURE__*/React.createElement(FreebieBand, {
    onNav: onNav
  }));
}
window.Home = Home;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Home.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/Illustration.jsx
try { (() => {
/* global React */
// Papier Pivoine — honest placeholder for the watercolour/line-art imagery
// that the brand centres on but that was not supplied as assets.
function Illustration({
  label = 'Illustration pivoine',
  height = 240,
  tone = 'blush',
  radius = 'var(--radius-md)',
  style = {}
}) {
  const fills = {
    blush: 'linear-gradient(145deg, var(--blush) 0%, var(--pale-rose) 120%)',
    sage: 'linear-gradient(145deg, var(--sage-soft) 0%, var(--sage) 140%)',
    warm: 'linear-gradient(145deg, var(--paper-warm) 0%, var(--blush) 130%)'
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height,
      borderRadius: radius,
      background: fills[tone] || fills.blush,
      border: '1px solid var(--border-faint)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
      ...style
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "56",
    height: "56",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "var(--rose)",
    strokeWidth: "1",
    opacity: "0.55",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M12 3c2.5 1.5 3 4 2 6 2-1 4 0 4.5 2 .5 2-1 4-3.5 4.5 1.5 1 1.5 3 .5 4.5-1.2 1.8-4 1.8-6 0-2 1.8-4.8 1.8-6 0-1-1.5-1-3.5.5-4.5C1.5 15 0 13 .5 11 1 9 3 8 5 9c-1-2-.5-4.5 2-6 1.6-1 3.4-1 5 0Z"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "2.4"
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      bottom: 10,
      left: 0,
      right: 0,
      textAlign: 'center',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      fontStyle: 'italic',
      color: 'var(--rose-deep)',
      opacity: 0.7
    }
  }, label, " \xB7 \xE0 fournir"));
}
window.Illustration = Illustration;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/Illustration.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/LetterPage.jsx
try { (() => {
/* global React, Illustration */
// Papier Pivoine — the freebie email capture, with a gentle thank-you state.
function LetterPage() {
  const {
    TextField,
    Checkbox,
    Button,
    LetterBlock,
    Card
  } = window.PapierPivoineDesignSystem_2e8f20;
  const [email, setEmail] = React.useState('');
  const [ok, setOk] = React.useState(true);
  const [sent, setSent] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 920,
      margin: '0 auto',
      padding: '72px 48px 96px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 56,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Illustration, {
    label: "Pivoine \xB7 trait fin",
    height: 360,
    radius: "var(--radius-lg)",
    tone: "warm"
  }), /*#__PURE__*/React.createElement("div", null, !sent ? /*#__PURE__*/React.createElement(Card, {
    tone: "paper",
    style: {
      padding: 'var(--space-7)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 14
    }
  }, "Le cadeau"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      margin: '0 0 16px',
      lineHeight: 1.18
    }
  }, "Une premi\xE8re le\xE7on, et quelques pages"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-muted)',
      lineHeight: 'var(--leading-relaxed)',
      margin: '0 0 26px'
    }
  }, "Laisse ton adresse, je t'envoie tout de suite de quoi commencer. Tu peux te d\xE9sinscrire quand tu veux, rien ne presse."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 18
    }
  }, /*#__PURE__*/React.createElement(TextField, {
    label: "Ton adresse e-mail",
    placeholder: "prenom@exemple.fr",
    value: email,
    onChange: e => setEmail(e.target.value)
  }), /*#__PURE__*/React.createElement(Checkbox, {
    label: "Oui, je veux recevoir la lettre.",
    checked: ok,
    onChange: e => setOk(e.target.checked)
  }), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    fullWidth: true,
    disabled: !email.includes('@'),
    onClick: () => setSent(true)
  }, "Recevoir le cadeau"))) : /*#__PURE__*/React.createElement(Card, {
    tone: "blush",
    style: {
      padding: 'var(--space-7)'
    }
  }, /*#__PURE__*/React.createElement(LetterBlock, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 0
    }
  }, "C'est envoy\xE9. Regarde dans ta bo\xEEte, il est d\xE9j\xE0 l\xE0."), /*#__PURE__*/React.createElement("p", null, "Prends ton temps avec. Il n'y a rien \xE0 faire ce soir, seulement l'ouvrir si tu en as envie."), /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 0
    }
  }, "Je suis contente que tu sois l\xE0."))))));
}
window.LetterPage = LetterPage;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/LetterPage.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/ProductPage.jsx
try { (() => {
/* global React, Illustration */
// Papier Pivoine — product detail (the flagship journal).
function ProductPage({
  onNav
}) {
  const {
    Button,
    Tag,
    PivoineBadge,
    Divider
  } = window.PapierPivoineDesignSystem_2e8f20;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1100,
      margin: '0 auto',
      padding: '64px 48px 88px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 64,
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Illustration, {
    label: "Couverture \xB7 aquarelle",
    height: 460,
    radius: "var(--radius-lg)"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Tag, {
    tone: "rose",
    style: {
      marginBottom: 18
    }
  }, "Le carnet"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-3xl)',
      lineHeight: 1.12,
      margin: '0 0 10px'
    }
  }, "Quand ma t\xEAte est pleine"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-lg)',
      color: 'var(--text-muted)',
      margin: '0 0 8px'
    }
  }, "Un carnet d'\xE9criture pour apaiser un esprit qui pense trop."), /*#__PURE__*/React.createElement("p", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 28
    }
  }, "Pour femmes hypersensibles et introverties"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-md)',
      color: 'var(--text-body)',
      lineHeight: 'var(--leading-relaxed)',
      maxWidth: '44ch',
      margin: '0 0 28px'
    }
  }, "Tu l'imprimes chez toi, tu le remplis \xE0 la main, il est \xE0 toi pour toujours. L\xE9ger en encre, beaucoup de blanc, de la place pour respirer. Tu l'ouvres quand tu veux, cinq minutes le soir ou un long dimanche."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 14,
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-2xl)',
      color: 'var(--deep-olive)'
    }
  }, "18 \u20AC"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      color: 'var(--text-faint)'
    }
  }, "PDF \xE0 imprimer \xB7 A4")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 14,
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "lg",
    onClick: () => onNav('letter')
  }, "T\xE9l\xE9charger le carnet"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "lg"
  }, "Version papier (Amazon)")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-faint)',
      margin: 0
    }
  }, "Tu pr\xE9f\xE8res un livre d\xE9j\xE0 imprim\xE9 ? Une \xE9dition broch\xE9e existe aussi."))), /*#__PURE__*/React.createElement(Divider, {
    ornament: true,
    spacing: "64px"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: 'center',
      marginBottom: 40
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "pp-eyebrow",
    style: {
      marginBottom: 14
    }
  }, "Ce que la page te permet"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 'var(--text-2xl)',
      margin: 0
    }
  }, "La m\xE9thode pivoine")), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 560,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement(PivoineBadge, {
    variant: "list"
  })));
}
window.ProductPage = ProductPage;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/ProductPage.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/SiteHeader.jsx
try { (() => {
/* global React */
// Papier Pivoine — site header. Wordmark in Aboreto, quiet nav.
function SiteHeader({
  onNav,
  current
}) {
  const link = (key, label) => /*#__PURE__*/React.createElement("button", {
    onClick: () => onNav(key),
    style: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-body)',
      fontSize: 'var(--text-sm)',
      letterSpacing: '0.02em',
      padding: '4px 0',
      color: current === key ? 'var(--rose)' : 'var(--text-muted)',
      borderBottom: current === key ? '1px solid var(--rose)' : '1px solid transparent',
      transition: 'color var(--dur-base) var(--ease-soft)'
    }
  }, label);
  return /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '22px 48px',
      borderBottom: '1px solid var(--border-faint)',
      background: 'var(--paper-warm)',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: () => onNav('home'),
    style: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-xl)',
      color: 'var(--deep-olive)',
      letterSpacing: '0.06em'
    }
  }, "Papier Pivoine"), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      gap: '32px',
      alignItems: 'center'
    }
  }, link('home', 'Accueil'), link('journal', 'Le carnet'), link('books', "Les cahiers"), link('letter', 'La lettre')));
}
window.SiteHeader = SiteHeader;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/SiteHeader.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Divider = __ds_scope.Divider;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.TextField = __ds_scope.TextField;

__ds_ns.Textarea = __ds_scope.Textarea;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.LetterBlock = __ds_scope.LetterBlock;

__ds_ns.PivoineBadge = __ds_scope.PivoineBadge;

})();
