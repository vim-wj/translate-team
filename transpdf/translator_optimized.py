"""
优化版翻译器 - 改进的 Prompt 设计，使翻译更贴近目标语言母语表达

基于 PDFMathTranslate 的 translator.py 进行优化：
1. 添加上下文理解指导
2. 添加母语化表达指导  
3. 添加专业术语处理
"""

from string import Template
from typing import cast, Optional


# ============================================================================
# 优化的 Prompt 模板
# ============================================================================

OPTIMIZED_PROMPT_TEMPLATE = Template("""你是一位专业的学术翻译专家，精通${lang_in}和${lang_out}。你的任务是将以下文本从${lang_in}翻译成${lang_out}。

## 翻译要求

### 1. 上下文理解
- 这段文本来自学术论文或技术文档
- 请理解整体语境，确保翻译符合学术写作规范
- 保持原文的逻辑结构和论证方式

### 2. 母语化表达
- 使用${lang_out}的自然表达方式，避免生硬的直译
- 句式应符合${lang_out}的语法习惯
- 用词应准确、专业、地道
- 避免"翻译腔"，让译文读起来像母语者写的

### 3. 专业术语处理
- 保持专业术语的准确性
- 对于有标准译法的术语，使用标准译名
- 对于没有标准译法的新术语，可在首次出现时保留原文并加注
- 同一术语在全文中保持一致的译法

### 4. 格式保留
- 保持 Markdown 格式不变
- 保持公式标记 {v*} 不变
- 保持引用、脚注等学术元素
- 保持代码块和技术标识符不变

### 5. 输出要求
- 只输出翻译结果，不要包含任何解释或额外文字
- 不要输出"翻译如下"等引导语
- 直接开始翻译内容

## 待翻译文本

${text}

## 翻译结果
""")

# 简洁版 Prompt（适用于短文本或需要快速翻译的场景）
SIMPLE_PROMPT_TEMPLATE = Template("""你是专业翻译引擎。将以下${lang_in}文本翻译成${lang_out}：
- 使用自然流畅的${lang_out}表达
- 保持专业术语准确
- 保留公式标记{v*}和 Markdown 格式
- 只输出译文，无额外内容

原文：${text}

译文：""")

# 详细版 Prompt（适用于重要文档或需要高质量翻译的场景）
DETAILED_PROMPT_TEMPLATE = Template("""你是一位经验丰富的${lang_in}→${lang_out}翻译专家，专门从事学术论文和技术文档的翻译工作。

## 原文信息
- 源语言：${lang_in}
- 目标语言：${lang_out}
- 文本类型：学术/技术文档

## 翻译准则

### 一、理解层面
1. **语境理解**：准确把握原文的学术语境和专业背景
2. **意图理解**：理解作者的表达意图和论证逻辑
3. **文化理解**：注意${lang_in}和${lang_out}之间的文化差异

### 二、表达层面
1. **母语化**：译文应符合${lang_out}母语者的表达习惯
   - 避免逐字翻译导致的生硬表达
   - 使用${lang_out}常用的句式和连接词
   - 注意语序的自然流畅

2. **专业性**：保持学术写作的严谨性
   - 使用规范的学术用语
   - 保持客观、准确的语气
   - 避免口语化表达

3. **一致性**：确保全文翻译风格统一
   - 术语译法前后一致
   - 语气风格保持连贯
   - 格式规范统一

### 三、技术细节
1. **公式和符号**：保持所有数学公式、代码、标记不变
2. **引用和注释**：保留原文的引用格式和注释结构
3. **图表引用**：保持"如图 X 所示"等引用的准确性

## 待翻译内容

${text}

## 输出要求
- 仅输出翻译结果
- 不包含任何解释、说明或额外文字
- 直接开始翻译内容

## 翻译结果
""")


# ============================================================================
# Prompt 优化函数
# ============================================================================

def get_optimized_prompt(template_type: str = "optimized") -> Template:
    """
    获取优化后的 Prompt 模板
    
    Args:
        template_type: 模板类型
            - "optimized": 优化版（平衡质量和速度）
            - "simple": 简洁版（快速翻译）
            - "detailed": 详细版（高质量翻译）
    
    Returns:
        Template 对象
    """
    if template_type == "simple":
        return SIMPLE_PROMPT_TEMPLATE
    elif template_type == "detailed":
        return DETAILED_PROMPT_TEMPLATE
    else:
        return OPTIMIZED_PROMPT_TEMPLATE


def create_custom_prompt(
    lang_in: str,
    lang_out: str,
    text: str,
    template: Optional[Template] = None,
    context: Optional[str] = None,
    terminology: Optional[dict] = None,
    style: Optional[str] = None
) -> list[dict[str, str]]:
    """
    创建自定义翻译 Prompt
    
    Args:
        lang_in: 源语言
        lang_out: 目标语言
        text: 待翻译文本
        template: 使用的模板，默认使用优化版
        context: 额外上下文信息（如文档类型、领域等）
        terminology: 专业术语字典 {原文：译文}
        style: 翻译风格（如"学术"、"技术"、"通俗"等）
    
    Returns:
        消息列表，可直接用于 LLM API
    """
    if template is None:
        template = OPTIMIZED_PROMPT_TEMPLATE
    
    # 基础替换
    content = template.safe_substitute({
        "lang_in": lang_in,
        "lang_out": lang_out,
        "text": text,
    })
    
    # 添加额外上下文
    if context:
        context_instruction = f"\n## 额外上下文\n{context}\n"
        content = content.replace("## 翻译要求", context_instruction + "\n## 翻译要求")
    
    # 添加术语表
    if terminology:
        term_list = "\n".join([f"- {k}: {v}" for k, v in terminology.items()])
        term_instruction = f"\n## 术语表\n请确保以下术语使用指定的译法：\n{term_list}\n"
        content = content.replace("### 3. 专业术语处理", term_instruction + "\n### 3. 专业术语处理")
    
    # 添加风格要求
    if style:
        style_instruction = f"- 翻译风格：{style}\n"
        content = content.replace("### 2. 母语化表达", style_instruction + "\n### 2. 母语化表达")
    
    return [
        {
            "role": "user",
            "content": content,
        }
    ]


def optimize_prompt_for_domain(
    text: str,
    lang_in: str,
    lang_out: str,
    domain: str = "academic"
) -> list[dict[str, str]]:
    """
    根据领域优化 Prompt
    
    Args:
        text: 待翻译文本
        lang_in: 源语言
        lang_out: 目标语言
        domain: 领域类型
            - "academic": 学术论文
            - "technical": 技术文档
            - "legal": 法律文件
            - "medical": 医学文献
            - "general": 通用
    
    Returns:
        优化后的消息列表
    """
    domain_instructions = {
        "academic": {
            "context": "这是一篇学术论文，包含研究背景、方法、结果和讨论。",
            "style": "学术严谨，使用规范的学术用语，保持客观语气",
            "terms": {
                "abstract": "摘要",
                "introduction": "引言",
                "methodology": "方法论",
                "results": "结果",
                "discussion": "讨论",
                "conclusion": "结论",
                "references": "参考文献",
            }
        },
        "technical": {
            "context": "这是一份技术文档，可能包含代码、API 说明或系统架构描述。",
            "style": "技术准确，简洁明了，便于理解和实施",
            "terms": {
                "API": "API（应用程序接口）",
                "SDK": "SDK（软件开发工具包）",
                "framework": "框架",
                "library": "库",
                "module": "模块",
                "function": "函数",
                "class": "类",
                "method": "方法",
            }
        },
        "legal": {
            "context": "这是一份法律文件，用词需要精确且符合法律规范。",
            "style": "法律正式用语，严谨准确，避免歧义",
            "terms": {}  # 法律术语因法域而异，需具体分析
        },
        "medical": {
            "context": "这是一份医学文献，包含医学术语和临床数据。",
            "style": "医学术语准确，符合医学写作规范",
            "terms": {
                "clinical trial": "临床试验",
                "placebo": "安慰剂",
                "efficacy": "疗效",
                "adverse effect": "不良反应",
                "dosage": "剂量",
            }
        },
        "general": {
            "context": None,
            "style": "自然流畅，通俗易懂",
            "terms": {}
        }
    }
    
    config = domain_instructions.get(domain, domain_instructions["general"])
    
    return create_custom_prompt(
        lang_in=lang_in,
        lang_out=lang_out,
        text=text,
        context=config["context"],
        style=config["style"],
        terminology=config["terms"] if config["terms"] else None
    )


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 测试优化后的 Prompt
    print("=" * 60)
    print("优化版翻译 Prompt 测试")
    print("=" * 60)
    
    # 测试基础模板
    template = get_optimized_prompt("optimized")
    print("\n【优化版模板】")
    print(template.safe_substitute({
        "lang_in": "English",
        "lang_out": "Chinese",
        "text": "This is a test sentence.",
    })[:500] + "...")
    
    # 测试自定义 Prompt
    print("\n【自定义 Prompt】")
    custom = create_custom_prompt(
        lang_in="English",
        lang_out="Chinese",
        text="The algorithm uses a dynamic programming approach.",
        context="这是一篇计算机科学论文",
        terminology={"algorithm": "算法", "dynamic programming": "动态规划"},
        style="学术严谨"
    )
    print(custom[0]["content"][:500] + "...")
    
    # 测试领域优化
    print("\n【学术领域优化】")
    academic = optimize_prompt_for_domain(
        text="We conducted a series of experiments to evaluate the performance.",
        lang_in="English",
        lang_out="Chinese",
        domain="academic"
    )
    print(academic[0]["content"][:500] + "...")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
