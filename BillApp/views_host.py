
       
def shareSalesReportsToEmail(request):
    if request.user:
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                # print(emails_list)

                cmp = Company.objects.get( user = request.user.id)
                invoices = Sales.objects.filter(cid=cmp)


                excelfile = BytesIO()
                workbook = Workbook()
                worksheet = workbook.active
                worksheet.title = 'Sales Reports'

                # Write headers
                headers = ['#', 'Date', 'Invoice Number', 'Party Name', 'Amount']
                for col_num, header in enumerate(headers, 1):
                    worksheet.cell(row=1, column=col_num, value=header)

                # Write sales invoices data
                for idx, invoice in enumerate(invoices, start=2):
                    worksheet.cell(row=idx, column=1, value=idx - 1)  # Index
                    worksheet.cell(row=idx, column=2, value=invoice.date)  # Date
                    worksheet.cell(row=idx, column=3, value=invoice.bill_number)  # Invoice Number
                    worksheet.cell(row=idx, column=4, value=invoice.party_name)  # Party Name
                    worksheet.cell(row=idx, column=5, value=invoice.total_amount)  # Amount

                

                # Save workbook to BytesIO object
                workbook.save(excelfile)
                mail_subject = f'Sales Reports - {date.today()}'
                message = f"Hi,\nPlease find the ALES REPORTS file attached. \n{email_message}\n\n--\nRegards,\n{cmp.company_name}\n{cmp.address}\n{cmp.state} - {cmp.country}\n{cmp.phone_number}"
                message = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, emails_list)
                message.attach(f'Sales Reports-{date.today()}.xlsx', excelfile.getvalue(), 'application/vnd.ms-excel')
                message.send(fail_silently=False)

                messages.success(request, 'Sales Report has been shared via email successfully..!')
                return redirect(Salesreport)
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while sharing the sales report via email.')

            return redirect(Salesreport)
