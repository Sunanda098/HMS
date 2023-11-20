from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openerp.tools as tools
import pymssql

class ResCompany(models.Model):
    _inherit = 'res.company'

    unipath_host = fields.Char("IP")
    unipath_port = fields.Char("Port", default='1433', help='1433')
    unipath_user = fields.Char("Username")
    unipath_password = fields.Char("Password")
    unipath_database = fields.Char("Database")

    @api.multi
    def test_unipath_connection(self):
        try:
            pymssql.connect(user=self.unipath_user, password=self.unipath_password, database=self.unipath_database, host=self.unipath_host, port=self.unipath_port)
        except Exception, e:
            raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % tools.ustr(e))
        raise UserError(_("Connection Test Succeeded! Everything seems properly set up!"))


class Investigation(models.Model):
    _inherit = 'hms.investigation'

    @api.multi
    def get_age_unit(self):
        b_date = datetime.strptime(self.patient_id.dob, '%Y-%m-%d')
        delta = relativedelta(datetime.now(), b_date)
        age = _("%syear") % (delta.years)
        return [delta.years, 'Yrs']

    @api.multi
    def button_accepted_xray(self):
        super(Investigation, self).button_accepted_xray()
        if self.investigation_type == 'pathology':
            ipopflag = self.hospitalization_id and 'IP' or 'OP'
            ref_visitno = (self.hospitalization_id and self.hospitalization_id.name) or (self.appointment_id and self.appointment_id.name)
            admissionno = self.hospitalization_id and self.hospitalization_id.name or 'Not Applicable'
            age = ""
            if self.patient_id.dob:
                age = self.get_age_unit()
            primary_physician = (self.hospitalization_id and self.hospitalization_id.primary_physician) or (self.appointment_id and self.appointment_id.physician_id)
            company = self.env.user.company_id
            # try:
            conn = pymssql.connect(user=company.unipath_user, password=company.unipath_password, database=company.unipath_database, host=company.unipath_host, port=company.unipath_port)
            cursor = conn.cursor()
            values = []
            for line in  self.pathology_line:
                values.append((
                        ipopflag, self.patient_id.zip, self.name, admissionno, self.date_investigation, line.product_id.id, 'N', line.product_id.name,
                        self.patient_id.first_name, self.patient_id.middel_name, self.patient_id.last_name, self.patient_id.sex.title(), age and str(age[0]), age and age[1], 'indian', self.patient_id.mobile, self.patient_id.mobile,
                        primary_physician and primary_physician.id or None, primary_physician and primary_physician.name or '', primary_physician and primary_physician.mobile or '',
                        '0'
                    ))
                print
            if values:
                query = """INSERT INTO i_table(ipopflag, pinno, ref_visitno, admissionno, reqdatetime, testprof_code, processed, package_name,
                    patfname, patmname, patlname, gender, patage, ageunitq, nationality, Teli_mobi, Patmobile,
                    refdoccode, doc_name, Docmobile,
                    Labno) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"""
                cursor.executemany(query,values)
                # you must call commit() to persist your data if you don't set autocommit to True
                conn.commit()
                conn.close()
            # except Exception, e:
            #     raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % tools.ustr(e))
