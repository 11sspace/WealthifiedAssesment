from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, BigInteger, VARCHAR, Date, Float, DateTime, Boolean, Text
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()
class MutualFundTransaction(db.Model, SerializerMixin):
    __tablename__ = "mutual_fund_transactions"
    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    amc_code = Column(Text)
    folio_no = Column(Text)
    prodcode = Column(Text)
    scheme = Column(Text)
    inv_name = Column(Text)
    trxntype = Column(Text)
    trxnno = Column(Text)
    trxnmode = Column(Text)
    trxnstat = Column(Text)
    usercode = Column(Text)
    usrtrxno = Column(Text)
    trad_date = Column(Date)
    post_date = Column(Date)
    pur_price = Column(Float)
    units = Column(Float)
    amount = Column(Float)
    brokcode = Column(Text)
    subbrok = Column(Text)
    brokperc = Column(Float)
    brokcomm = Column(Float)
    altfolio = Column(Text)
    rep_date = Column(Date)
    time1 = Column(Text)
    trxnsubtyp = Column(Text)
    application_no = Column(Text)
    trxn_nature = Column(Text)
    tax = Column(Float)
    total_tax = Column(Float)
    te_15h = Column(Text)
    micr_no = Column(Text)
    remarks = Column(Text)
    swflag = Column(Text)
    old_folio = Column(Text)
    seq_no = Column(Text)
    reinvest_flag = Column(Text)
    mult_brok = Column(Text)
    stt = Column(Float)
    location = Column(Text)
    scheme_type = Column(Text)
    tax_status = Column(Text)
    load = Column(Float)
    scanrefno = Column(Text)
    pan = Column(Text)
    inv_iin = Column(Text)
    targ_src_scheme = Column(Text)
    trxn_type_flag = Column(Text)
    ticob_trtype = Column(Text)
    ticob_trno = Column(Text)
    ticob_posted_date = Column(Date)
    dp_id = Column(Text)
    trxn_charges = Column(Float)
    eligib_amt = Column(Float)
    src_of_txn = Column(Text)
    trxn_suffix = Column(Text)
    siptrxnno = Column(Text)
    ter_location = Column(Text)
    euin = Column(Text)
    euin_valid = Column(Text)
    euin_opted = Column(Text)
    sub_brk_arn = Column(Text)
    exch_dc_flag = Column(Text)
    src_brk_code = Column(Text)
    sys_regn_date = Column(Date)
    ac_no = Column(Text)
    bank_name = Column(Text)
    reversal_code = Column(Text)
    exchange_flag = Column(Text)
    ca_initiated_date = Column(Date)
    gst_state_code = Column(Text)
    igst_amount = Column(Float)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    rev_remark = Column(Text)
    original_trxnno = Column(Text)
    stamp_duty = Column(Float)
    folio_old = Column(Text)
    scheme_folio_number = Column(Text)
    amc_ref_no = Column(Text)
    request_ref_no = Column(Text)
    created_on = Column(DateTime)
    created_by = Column(Text)
    modified_on = Column(DateTime)
    modified_by = Column(Text)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)