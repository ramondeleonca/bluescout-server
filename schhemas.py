from schema import Schema, And, Use, Optional, SchemaError

bs_qr_code = Schema({
    "bs_qr_ver": And(Use(int)),
    "data": And(Use(str))
}, ignore_extra_keys=True, name="BlueScout QR code")