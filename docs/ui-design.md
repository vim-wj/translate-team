# transpdf UI Design Document

## 1. Design Philosophy

### 1.1 Core Principles
- **Minimalism**: Remove all non-essential elements, focus on core translation functionality
- **AI/Tech Aesthetic**: Create a futuristic, intelligent feel through visual design
- **User-Centric**: Streamlined workflow with intuitive interactions
- **Performance**: Fast loading, responsive interface, real-time feedback

### 1.2 Removed Elements (vs. Original PDFMathTranslate)
- ❌ Document preview panel
- ❌ Model selection dropdown
- ❌ Complex experimental options accordion
- ❌ reCAPTCHA verification
- ❌ Link input option (file upload only)
- ❌ BabelDOC toggle
- ❌ Environment variable configuration panels
- ❌ Technical details footer

## 2. Color Scheme

### 2.1 Primary Palette

| Color | Hex Code | Usage |
|-------|----------|-------|
| **Deep Space** | `#0a0e1a` | Background gradient (dark) |
| **Nebula** | `#1a1f2e` | Background gradient (light) |
| **Cyan Neon** | `#00f2fe` | Primary accent, highlights |
| **Electric Blue** | `#4facfe` | Secondary accent, borders |
| **Purple Haze** | `#667eea` | Secondary button gradient |
| **Violet Storm** | `#764ba2` | Secondary button gradient |
| **Success Green** | `#00ff88` | Success states, download area |
| **Error Red** | `#ff4757` | Error states, warnings |

### 2.2 Gradient Definitions

**Primary Button (Translate Now):**
```css
background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
box-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
```

**Secondary Button (Cancel):**
```css
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
```

**Progress Bar:**
```css
background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
box-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
```

### 2.3 Dark Theme Rationale

The dark background serves multiple purposes:
1. **Reduced Eye Strain**: Users often work with PDFs for extended periods
2. **Enhanced Contrast**: Neon accents pop against dark backgrounds
3. **Modern Aesthetic**: Aligns with AI/tech product conventions
4. **Focus**: Dark backgrounds minimize visual distractions

## 3. Layout Structure

### 3.1 Two-Column Layout

```
┌─────────────────────────────────────────────────────────┐
│                    HEADER                                │
│  ⚡ transpdf                                              │
│  AI-Powered PDF Translation | Fast • Simple • Accurate  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────┬───────────────────────────────────┐
│   COLUMN 1 (50%)    │      COLUMN 2 (50%)               │
│                     │                                   │
│  📁 Upload PDF      │   📊 Progress                     │
│  [File Drop Zone]   │   *Ready to translate*            │
│                     │                                   │
│  ⚙️ Settings        │   📥 Download (hidden initially)  │
│  - Service          │   [Mono PDF]                      │
│  - From/To Language │   [Dual PDF]                      │
│  - Page Range       │                                   │
│                     │                                   │
│  🚀 Actions         │                                   │
│  [Translate Now]    │                                   │
│  [Cancel]           │                                   │
└─────────────────────┴───────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                    FOOTER                                │
│  transpdf v1.0 | Powered by PDFMathTranslate vX.X       │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Responsive Behavior

- **Desktop (>1024px)**: Two-column side-by-side layout
- **Tablet (768px-1024px)**: Stacked columns with adjusted spacing
- **Mobile (<768px)**: Single column, vertical stacking

### 3.3 Component Hierarchy

1. **Header Section**
   - Product name with emoji icon (⚡ transpdf)
   - Tagline emphasizing key benefits

2. **Input Section (Left Column)**
   - File upload area (prominent, dashed border)
   - Translation settings (dropdowns)
   - Page range selector (radio + conditional textbox)
   - Action buttons (primary + secondary)

3. **Output Section (Right Column)**
   - Progress status (text feedback)
   - Download area (conditionally visible)
   - Version information

## 4. Component Specifications

### 4.1 File Upload Area

**Visual Design:**
- Height: 200px
- Border: 2px dashed `#00f2fe`
- Background: `rgba(0, 242, 254, 0.05)`
- Border Radius: 12px
- Hover Effect: Glow intensifies, background brightens

**Interaction:**
- Drag & drop support
- Click to open file picker
- PDF-only file type restriction
- Single file limit

**Hover State:**
```css
border-color: #4facfe;
background: rgba(0, 242, 254, 0.1);
box-shadow: 0 0 30px rgba(0, 242, 254, 0.2);
```

### 4.2 Dropdown Menus

**Styling:**
- Border: 1px solid `#4facfe`
- Background: `rgba(26, 31, 46, 0.8)`
- Border Radius: 8px
- Label Color: `#00f2fe` (neon cyan)

**Options:**
- Service: Google, Bing, DeepL, OpenAI, Gemini, etc.
- Languages: 10 most common languages
- Default: English → Simplified Chinese

### 4.3 Page Range Selector

**Radio Options:**
1. **全部** (All) - Default, no page limit
2. **前 N 页** (First N Pages) - Shows numeric input
3. **自定义范围** (Custom Range) - Shows text input for ranges

**Conditional Display:**
- "前 N 页" → Textbox: "Enter number of pages (e.g., 5)"
- "自定义范围" → Textbox: "Enter page range... (e.g., 1-5 or 1,3,5)"
- "全部" → Textbox hidden

### 4.4 Action Buttons

**Primary Button (Translate Now):**
- Size: Large
- Variant: Primary
- Icon: ⚡ (lightning bolt)
- Gradient: Cyan to blue
- Glow Effect: Neon shadow
- Text: "⚡ Translate Now"

**Secondary Button (Cancel):**
- Size: Large
- Variant: Secondary
- Icon: ⏹️ (stop button)
- Gradient: Purple to violet
- Initially Hidden
- Shows during translation

### 4.5 Progress Display

**Location:** Right column top
**Format:** Markdown text with dynamic updates
**States:**
- Idle: "*Ready to translate*"
- Processing: "🚀 Starting translation..." → "Translating... (X%)"
- Complete: "✅ Translation complete!"
- Error: "❌ Translation failed: [error message]"

### 4.6 Download Area

**Visibility:** Hidden until translation completes

**Styling:**
- Border: 2px solid `#00ff88` (success green)
- Background: `rgba(0, 255, 136, 0.05)`
- Padding: 20px
- Border Radius: 12px
- Margin Top: 20px

**File Links:**
1. 📄 Translated PDF (Mono) - Single language version
2. 📄 Translated PDF (Dual Language) - Bilingual version

## 5. Interaction Design

### 5.1 User Flow

```
1. User arrives at page
   ↓
2. Upload PDF file (drag or click)
   ↓
3. Configure settings (optional - defaults work)
   - Select service
   - Select languages
   - Select page range
   ↓
4. Click "⚡ Translate Now"
   ↓
5. Watch progress (real-time updates)
   ↓
6. Download translated file(s)
```

### 5.2 Event Handlers

**Page Option Change:**
```python
on_page_option_change(choice):
    if choice == "自定义范围":
        show textbox (placeholder: "Enter page range...")
    elif choice == "前 N 页":
        show textbox (placeholder: "Enter number of pages (e.g., 5)")
    else:
        hide textbox
```

**Translation Start:**
- Validate file upload
- Generate session ID
- Create cancellation event
- Show progress bar
- Disable translate button
- Show cancel button

**Translation Complete:**
- Hide progress bar
- Show download area
- Enable file download links
- Hide cancel button
- Show success message

**Translation Cancel:**
- Trigger cancellation event
- Clean up session state
- Show cancellation message
- Reset button states

### 5.3 Error Handling

**Validation Errors:**
- No file uploaded → "❌ No file uploaded"
- Invalid page range → "❌ Invalid page specification"
- Translation service error → "❌ Translation failed: [details]"

**Visual Feedback:**
- Error messages in red (`#ff4757`)
- Success messages in green (`#00ff88`)
- Progress updates in cyan (`#00f2fe`)

## 6. Technical Implementation

### 6.1 Framework

- **Library:** Gradio (Python)
- **Theme:** Custom Base theme with neon accents
- **Layout:** Blocks API with Row/Column structure
- **Styling:** Custom CSS + Gradio theme colors

### 6.2 Key Dependencies

```python
import gradio as gr
from pdf2zh import __version__
from pdf2zh.high_level import translate
from pdf2zh.doclayout import ModelInstance
from pdf2zh.config import ConfigManager
from pdf2zh.translator import [...]
```

### 6.3 State Management

**Session State:**
```python
state = gr.State({"session_id": None})
```

**Cancellation Tracking:**
```python
cancellation_event_map = {}  # session_id → asyncio.Event
```

### 6.4 Server Configuration

**Default Settings:**
- Port: 7860
- Server: 0.0.0.0 (fallback to 127.0.0.1)
- Debug: True
- In-browser: True
- Share: False (configurable)

**Fallback Strategy:**
1. Try 0.0.0.0 (all interfaces)
2. Fallback to 127.0.0.1 (localhost)
3. Final fallback to share=True (public link)

## 7. Accessibility Considerations

### 7.1 Color Contrast

- Text on background: WCAG AA compliant
- Neon accents used for decoration, not critical info
- Error states use both color and icons

### 7.2 Keyboard Navigation

- All interactive elements keyboard accessible
- Tab order follows visual flow (left to right, top to bottom)
- Focus indicators visible on all elements

### 7.3 Screen Reader Support

- All form elements have associated labels
- Icons accompanied by text descriptions
- Progress updates announced dynamically

## 8. Performance Optimizations

### 8.1 Loading Strategy

- Minimal initial payload (no preview component)
- Lazy loading for download section
- CSS inlined for single request

### 8.2 Resource Management

- Single file processing (no batch overhead)
- Automatic cleanup of temporary files
- Session-based cancellation for resource release

### 8.3 Network Efficiency

- Default thread count: 4 (balanced performance)
- Progress callbacks optimized for UI updates
- No external CDN dependencies

## 9. Future Enhancements

### 9.1 Potential Additions

- [ ] Batch file processing
- [ ] Translation history/log
- [ ] Custom glossary support
- [ ] Side-by-side comparison view
- [ ] Export format options
- [ ] API key management UI
- [ ] Multi-language UI support

### 9.2 Advanced Features (Not in MVP)

- [ ] Real-time preview of translated pages
- [ ] Translation quality scoring
- [ ] A/B testing of different services
- [ ] Usage analytics dashboard
- [ ] Team collaboration features

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-09 | Initial release - simplified GUI |

---

**Design Team:** transpdf Project  
**Based On:** PDFMathTranslate (Byaidu/PDFMathTranslate)  
**License:** Follow original project license

