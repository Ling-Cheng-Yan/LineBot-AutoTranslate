from googletrans import Translator
translator = Translator()
result = translator.detect("我喜歡打英雄聯盟")
print(result.lang)