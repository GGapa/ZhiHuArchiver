def get_personal_tags() -> str:
    """
    返回自定义 HTML 标签，插入到每个页面的 <head> 中。

    你可以在此函数中添加任何自定义的 meta 标签、脚本、统计代码等。
    例如：
    - Google Search Console 验证
    - Google Analytics / gtag
    - 自定义 meta 标签

    如果不想要任何自定义标签，让此函数返回空字符串即可。
    """
    # === 示例：Google Search Console 验证 ===
    # 取消下面的注释并填写你的验证码
    # return '<meta name="google-site-verification" content="your_verification_code" />'

    # === Google Search Console 验证 ===
    return '<meta name="google-site-verification" content="2AaB6pBizmqtxQRuLfFAkoA423iRVMVK3JT_GqSp_M8" />'
