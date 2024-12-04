# utils.py
def clean_text(content):
    return re.sub(r'[\[\]\\\\n\"\'\n]', '', content)
# 텍스트에서 불필요한 문자 제거