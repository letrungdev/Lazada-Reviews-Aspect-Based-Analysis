from underthesea import sentiment


object_name = "máy tính"
aspect = "màn hình"
value = "khá đẹp"

text = aspect + " của " + object_name + " " + value
print(text)
print(sentiment(text))

