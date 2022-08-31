from pdf2image import convert_from_path


# конвертирует из PDF в JPG
def converter():

    images = convert_from_path("images\\doc.pdf", 500)
    count_pages = 0

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('page' + str(i+1) + '.jpg')
        count_pages += 1

    return count_pages
