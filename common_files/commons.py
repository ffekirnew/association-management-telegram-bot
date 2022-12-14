from functions.assistor_functions import *

admin_question_emoji = 'đ'
answer_emoji = 'âī¸'
comment_emoji = 'đ'
question_emoji = 'â'
info_emoji = 'âšī¸'
admin_emoji = 'đ¨đŊâđģ'
back_button_emoji = 'âī¸'

back_markup = create_buttons(["{} go back.".format(back_button_emoji)], 1)
admin_home_markup = create_buttons(["{} add question".format(admin_question_emoji), "{} to see answers".format(answer_emoji), "{} to see comments".format(comment_emoji), "{} to see asked questions".format(question_emoji), "{} to add information".format(info_emoji)], 3)
user_home_markup = create_buttons(["{} to answer".format(answer_emoji), "{} to give comment".format(comment_emoji), "{} to ask a question".format(question_emoji), "{} to get info.".format(info_emoji)], 2)