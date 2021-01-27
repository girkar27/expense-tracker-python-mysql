
def month_func(code):
	month_dict = {
		'01': "January",
		'02': "February",
		'03': "MArch",
		'04': "April",
		'05': "May",
		'06': "June",
		'07': "July",
		'08': "August",
		'09': "September",
		'10': "October",
		'11': "November",
		'12': "December",
	}
	
	if code in month_dict:
		return month_dict[code]
	else:
		return "error"
