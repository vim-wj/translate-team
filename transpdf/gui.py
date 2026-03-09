"""
transpdf - Simplified PDF Translation GUI
Based on PDFMathTranslate, streamlined for essential functionality
"""

import os
import shutil
import uuid
from pathlib import Path
from asyncio import CancelledError
import logging

import gradio as gr
from pdf2zh import __version__
from transpdf.high_level import translate
from transpdf.doclayout import ModelInstance
from transpdf.config import ConfigManager
from transpdf.translator import (
    GoogleTranslator,
    BingTranslator,
    DeepLTranslator,
    DeepLXTranslator,
    OpenAITranslator,
    GeminiTranslator,
    AzureTranslator,
    TencentTranslator,
    ZhipuTranslator,
    SiliconTranslator,
)

logger = logging.getLogger(__name__)

# Service mapping (simplified - most common translators)
service_map = {
    "Google": GoogleTranslator,
    "Bing": BingTranslator,
    "DeepL": DeepLTranslator,
    "DeepLX": DeepLXTranslator,
    "OpenAI": OpenAITranslator,
    "Gemini": GeminiTranslator,
    "Azure": AzureTranslator,
    "Tencent": TencentTranslator,
    "Zhipu": ZhipuTranslator,
    "Silicon": SiliconTranslator,
}

# Language mapping
lang_map = {
    "Simplified Chinese": "zh",
    "Traditional Chinese": "zh-TW",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Spanish": "es",
    "Italian": "it",
}

# Cancellation event map
cancellation_event_map = {}


# Custom theme - Dark with neon accents (AI/Tech aesthetic)
custom_blue = gr.themes.Color(
    c50="#E8F3FF",
    c100="#BEDAFF",
    c200="#94BFFF",
    c300="#6AA1FF",
    c400="#4080FF",
    c500="#165DFF",
    c600="#0E42D2",
    c700="#0A2BA6",
    c800="#061D79",
    c900="#03114D",
    c950="#020B33",
)

custom_css = """
    /* Dark theme with neon accents */
    body {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
    }
    
    .gradio-container {
        background: transparent !important;
    }
    
    /* Neon accent colors */
    .primary-btn {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.3) !important;
    }
    
    .secondary-btn {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
    }
    
    /* File upload area */
    .input-file {
        border: 2px dashed #00f2fe !important;
        border-radius: 12px !important;
        background: rgba(0, 242, 254, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .input-file:hover {
        border-color: #4facfe !important;
        background: rgba(0, 242, 254, 0.1) !important;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.2) !important;
    }
    
    /* Dropdown styling */
    .dropdown {
        border: 1px solid #4facfe !important;
        border-radius: 8px !important;
        background: rgba(26, 31, 46, 0.8) !important;
    }
    
    /* Progress bar */
    .progress-bar-wrap {
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    .progress-bar {
        border-radius: 12px !important;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.5) !important;
    }
    
    /* Text inputs */
    input[type="text"], textarea {
        border: 1px solid #4facfe !important;
        border-radius: 8px !important;
        background: rgba(26, 31, 46, 0.6) !important;
        color: #ffffff !important;
    }
    
    /* Labels */
    label {
        color: #00f2fe !important;
        font-weight: 600 !important;
    }
    
    /* Footer hidden */
    footer {
        visibility: hidden !important;
    }
    
    /* Accordion styling */
    .accordion {
        border: 1px solid #4facfe !important;
        border-radius: 8px !important;
    }
    
    /* Status messages */
    .status-success {
        color: #00ff88 !important;
    }
    
    .status-error {
        color: #ff4757 !important;
    }
    
    /* Download area */
    .download-area {
        border: 2px solid #00ff88 !important;
        border-radius: 12px !important;
        background: rgba(0, 255, 136, 0.05) !important;
        padding: 20px !important;
        margin-top: 20px !important;
    }
"""


def stop_translate_file(state: dict) -> None:
    """Stop the translation process"""
    session_id = state.get("session_id")
    if session_id is None:
        return
    if session_id in cancellation_event_map:
        logger.info(f"Stopping translation for session {session_id}")
        cancellation_event_map[session_id].set()


def translate_file(
    file_input,
    service,
    lang_from,
    lang_to,
    page_option,
    page_custom,
    state,
    progress=gr.Progress(),
):
    """
    Translate a PDF file from one language to another.
    
    Simplified translation function with essential parameters only.
    """
    session_id = uuid.uuid4()
    state["session_id"] = session_id
    cancellation_event_map[session_id] = CancelledError()
    
    progress(0, desc="🚀 Starting translation...")
    
    # Setup output directory
    output = Path("transpdf_output")
    output.mkdir(parents=True, exist_ok=True)
    
    # Validate input
    if not file_input:
        raise gr.Error("❌ No file uploaded")
    
    # Copy file to output directory
    file_path = shutil.copy(file_input, output)
    filename = os.path.splitext(os.path.basename(file_path))[0]
    file_raw = output / f"{filename}.pdf"
    file_mono = output / f"{filename}-mono.pdf"
    file_dual = output / f"{filename}-dual.pdf"
    
    # Get translator
    translator = service_map[service]
    
    # Process page range
    selected_page = None
    if page_option == "前 N 页":
        n_pages = min(5, int(page_custom) if page_custom.isdigit() else 5)
        selected_page = list(range(0, n_pages))
    elif page_option == "自定义范围":
        selected_page = []
        for p in page_custom.split(","):
            p = p.strip()
            if "-" in p:
                start, end = p.split("-")
                selected_page.extend(range(int(start) - 1, int(end)))
            elif p.isdigit():
                selected_page.append(int(p) - 1)
    
    # Set languages
    lang_in = lang_map[lang_from]
    lang_out = lang_map[lang_to]
    
    # Progress callback
    def progress_bar(t):
        desc = getattr(t, "desc", "Translating...")
        if desc == "":
            desc = "Translating..."
        progress(t.n / t.total, desc=desc)
    
    # Translation parameters
    param = {
        "files": [str(file_raw)],
        "pages": selected_page,
        "lang_in": lang_in,
        "lang_out": lang_out,
        "service": f"{translator.name}",
        "output": output,
        "thread": 4,
        "callback": progress_bar,
        "cancellation_event": cancellation_event_map[session_id],
        "envs": {},
        "prompt": None,
        "skip_subset_fonts": False,
        "ignore_cache": False,
        "model": ModelInstance.value,
    }
    
    try:
        translate(**param)
    except CancelledError:
        del cancellation_event_map[session_id]
        raise gr.Error("Translation cancelled by user")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise gr.Error(f"Translation failed: {str(e)}")
    
    # Verify output files exist
    if not file_mono.exists():
        raise gr.Error("Translation failed - no output file generated")
    
    progress(1.0, desc="✅ Translation complete!")
    
    # Return download links
    return (
        str(file_mono),
        str(file_mono),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
    )


def create_gui():
    """Create the simplified transpdf GUI"""
    
    with gr.Blocks(
        title="transpdf - AI PDF Translator",
        theme=gr.themes.Base(
            primary_hue=custom_blue,
            spacing_size="md",
            radius_size="lg",
        ),
        css=custom_css,
    ) as demo:
        
        # Header
        gr.Markdown(
            """
            # <span style="color: #00f2fe;">⚡ transpdf</span>
            ### AI-Powered PDF Translation | Fast • Simple • Accurate
            """,
            elem_classes=["header-text"],
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # File Upload Section
                gr.Markdown("### 📁 Upload PDF")
                file_input = gr.File(
                    label="Drop PDF here or click to upload",
                    file_count="single",
                    file_types=[".pdf"],
                    type="filepath",
                    elem_classes=["input-file"],
                    height=200,
                )
                
                # Translation Options
                gr.Markdown("### ⚙️ Translation Settings")
                
                service = gr.Dropdown(
                    label="Translation Service",
                    choices=list(service_map.keys()),
                    value="Google",
                    elem_classes=["dropdown"],
                )
                
                with gr.Row():
                    lang_from = gr.Dropdown(
                        label="From Language",
                        choices=list(lang_map.keys()),
                        value="English",
                        elem_classes=["dropdown"],
                    )
                    lang_to = gr.Dropdown(
                        label="To Language",
                        choices=list(lang_map.keys()),
                        value="Simplified Chinese",
                        elem_classes=["dropdown"],
                    )
                
                # Page Selection
                gr.Markdown("### 📄 Page Range")
                page_option = gr.Radio(
                    choices=["全部", "前 N 页", "自定义范围"],
                    label="Select Pages",
                    value="全部",
                )
                
                page_custom = gr.Textbox(
                    label="Page Specification (e.g., 1-5 or 1,3,5)",
                    placeholder="Enter page range...",
                    visible=False,
                    elem_classes=["text-input"],
                )
                
                # Action Buttons
                gr.Markdown("### 🚀 Start Translation")
                translate_btn = gr.Button(
                    "⚡ Translate Now",
                    variant="primary",
                    elem_classes=["primary-btn"],
                    size="lg",
                )
                
                cancel_btn = gr.Button(
                    "⏹️ Cancel",
                    variant="secondary",
                    elem_classes=["secondary-btn"],
                    visible=False,
                )
                
            with gr.Column(scale=1):
                # Status & Progress
                gr.Markdown("### 📊 Progress")
                progress_status = gr.Markdown(
                    "*Ready to translate*",
                    elem_classes=["status-text"],
                )
                
                # Download Section (initially hidden)
                download_section = gr.Markdown("### 📥 Download", visible=False)
                
                output_file_mono = gr.File(
                    label="📄 Translated PDF (Mono)",
                    visible=False,
                    elem_classes=["download-area"],
                )
                
                output_file_dual = gr.File(
                    label="📄 Translated PDF (Dual Language)",
                    visible=False,
                    elem_classes=["download-area"],
                )
                
                # Version info
                gr.Markdown(
                    f"""
                    ---
                    <div style="text-align: center; color: #666; font-size: 12px;">
                        transpdf v1.0 | Powered by PDFMathTranslate v{__version__}
                    </div>
                    """,
                )
        
        # State management
        state = gr.State({"session_id": None})
        
        # Event handlers
        def on_page_option_change(choice):
            """Show/hide custom page input based on selection"""
            if choice == "自定义范围":
                return gr.update(visible=True)
            elif choice == "前 N 页":
                return gr.update(visible=True, placeholder="Enter number of pages (e.g., 5)")
            else:
                return gr.update(visible=False)
        
        page_option.change(
            on_page_option_change,
            inputs=[page_option],
            outputs=[page_custom],
        )
        
        # Translation button click
        translate_btn.click(
            translate_file,
            inputs=[
                file_input,
                service,
                lang_from,
                lang_to,
                page_option,
                page_custom,
                state,
            ],
            outputs=[
                output_file_mono,
                output_file_dual,
                output_file_mono,
                output_file_dual,
                download_section,
            ],
        )
        
        # Cancel button click
        cancel_btn.click(
            stop_translate_file,
            inputs=[state],
            outputs=[],
        )
    
    return demo


def setup_gui(share: bool = False, server_port: int = 7860) -> None:
    """
    Setup and launch the GUI.
    
    Args:
        share: Whether to create a public shareable link
        server_port: Port number for the server
    """
    demo = create_gui()
    
    try:
        demo.launch(
            server_name="0.0.0.0",
            debug=True,
            inbrowser=True,
            share=share,
            server_port=server_port,
        )
    except Exception as e:
        logger.error(f"Failed to launch on 0.0.0.0: {e}")
        try:
            demo.launch(
                server_name="127.0.0.1",
                debug=True,
                inbrowser=True,
                share=share,
                server_port=server_port,
            )
        except Exception as e:
            logger.error(f"Failed to launch on 127.0.0.1: {e}")
            demo.launch(
                debug=True,
                inbrowser=True,
                share=True,
                server_port=server_port,
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_gui()
