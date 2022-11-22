from datetime import datetime

payment_log_path = "./logs/payment_log.txt"



def write_to_payment_log(user: str, command: str) -> None:

	f = open(payment_log_path, "a")
	current_time = datetime.now()
	date_time_string = current_time.strftime("%d/%m/%Y at %H:%M:%S")

	f.write(f'User: {user}    Command used: ${command}    Date & Time used: {date_time_string}' + "\n")
	f.close()


def clear_log_file() -> None:

	open(payment_log_path, "w").close()
