from fpdf import FPDF
from datetime import datetime
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))


def make_pdf(name, client_id, address, summ):
    pdf = FPDF()
    pdf.add_page()

    pdf.image(os.path.join(file_dir, r"invoice\logo.jpg"), 10, 8, 20)
    pdf.add_font('DejaVu', '', os.path.join(file_dir, r"invoice\DejaVuSansCondensed.ttf"), uni=True)
    pdf.add_font('DejaVuSerif-Bold', '', os.path.join(file_dir, r"invoice\DejaVuSans-Bold.ttf"), uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 50, 'Жилищно-управляющая компания "УК СПЕШЛКОМФОРТ"', 0, 1, 'L')
    pdf.ln(5)

    pdf.set_font('DejaVuSerif-Bold', '', 14)
    pdf.cell(0, 10, 'Квитанция на оплату услуг ЖКХ', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('DejaVu', '', 14)

    pdf.cell(90, 10, 'ФИО пользователя услуг:', 0, 0, 'L')
    pdf.cell(0, 10, name, 0, 1, 'R')

    pdf.cell(90, 10, 'Номер договора:', 0, 0, 'L')
    pdf.cell(0, 10, str(client_id), 0, 1, 'R')

    pdf.cell(90, 10, 'Адрес проживания:', 0, 0, 'L')
    pdf.cell(0, 10, address, 0, 1, 'R')

    pdf.cell(90, 10, 'Сумма оплаты:', 0, 0, 'L')
    pdf.cell(0, 10, f'{summ} рублей', 0, 1, 'R')


    cur_date = datetime.utcnow()
    pdf.cell(90, 10, 'Дата оплаты:', 0, 0, 'L')
    pdf.cell(0, 10, cur_date.strftime('%d.%m.%Y'), 0, 1, 'R')

    pdf.output(os.path.join(file_dir, r"invoice\demo.pdf"))
