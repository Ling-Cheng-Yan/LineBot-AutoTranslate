from googletrans import Translator
translator = Translator()
result = translator.detect("你好")
print(result.lang)