def translate(text):
    translations = ""
    for char in text:
        if char.lower() in "áàảãạắằẳẵặâấầẩẫậ":
            if char.isupper():
                translations = translations + "A"
            else:
                translations = translations + "a"
        else:
            translations = translations + char
    return translations

print(translate("SÁNG")
      )