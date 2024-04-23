import fitz
import pandas as pd

def convert_pdf_to_csv(pdf_file, csv_file):
    doc = fitz.open(pdf_file)
    main=[]
    # page=doc[0]
    # tabs = page.find_tables()
    # rows=tabs[0].extract()
    # main+=rows
    for page_no in range(len(doc)):
        tabs = doc[page_no].find_tables()
        rows=tabs[0].extract()
        if page_no==0:
            main.append(rows[0])
        main+=rows[1:]
        # print(page_no)
    doc.close()
    with open(csv_file, 'w', encoding='utf-8') as f:
        for row in main:
            for i in range(len(row)):
                f.write("\""+row[i]+"\",")
            f.write("\n")


convert_pdf_to_csv("EB_Redemption_Details.pdf","EB_Redemption_Details.csv")
print("File 1 - Saved to CSV")
convert_pdf_to_csv("EB_Purchase_Details.pdf","EB_Purchase_Details.csv")
print("File 2 - Saved to CSV")


# to remove unnecessary newline characters from the table headers
df=pd.read_csv("EB_Redemption_Details.csv")
print(df.columns)
df.rename(columns={'Date of\r\nEncashment':'Date of Encashment', 'Account no. of\r\nPolitical Party':'Account no. of Political Party','Bond\r\nNumber':'Bond Number','Pay Branch\r\nCode':'Pay Branch Code'},inplace=True)
df.drop(columns=["Unnamed: 9"],inplace=True)
print(df)
df.to_csv("EB_Redemption_Details.csv",index=False)

df=pd.read_csv("EB_Purchase_Details.csv")
print(df.columns)
df.rename(columns={'Date of\r\nPurchase':'Date of Purchase','Bond\r\nNumber':'Bond Number'},inplace=True)
df.drop(columns=["Unnamed: 12"],inplace=True)
print(df)
df.to_csv("EB_Purchase_Details.csv",index=False)
