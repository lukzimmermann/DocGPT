from src.utils.mail import send_mail

message = """\
Subject: Hi there

This message is sent from Python."""

send_mail("luk.zimmermann@gmx.ch", message)
