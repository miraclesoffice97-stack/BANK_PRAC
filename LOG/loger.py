import logging

loger = logging.getLogger("logg")

loger.setLevel(logging.DEBUG)

filerror = logging.FileHandler("signup_error_record.log")

infofile = logging.FileHandler("signup_Info_record.log")

filerror.setLevel(logging.ERROR)

infofile.setLevel(logging.INFO)

loger.addHandler(filerror)

loger.addHandler(infofile)


loginloger = logging.getLogger("loginlog")

loginloger.setLevel(logging.DEBUG)


loginfo = logging.FileHandler("login_rec.log")

logerror = logging.FileHandler("login_errors.log")


loginfo.setLevel(logging.INFO)

logerror.setLevel(logging.ERROR)

loginloger.addHandler(loginfo)

loginloger.addHandler(logerror)

