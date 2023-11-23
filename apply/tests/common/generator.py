from table.models import Post, Section, LongSentence, CheckBox, CheckBoxOption, File

def create_post(crew):
    return Post.objects.create(id=1,
                            apply_start_date="1000-01-01 00:00:00",
                            apply_end_date="1000-01-01 00:00:00",
                            document_result_date="1000-01-01 00:00:00",
                            has_interview=False,
                            requirement_target="0",
                            title="0",
                            content="0",
                            membership_fee="0",
                            crew=crew,
                            progress="0")

def create_section(id, section_name, post):
    return Section.objects.create(id=id,
                                  section_name=section_name,
                                  post=post,
                                  description="테스트용 섹션입니다.")

def create_long_question(content, sequence, section):
    return LongSentence.objects.create(question=content,
                                       letter_count_limit=500,
                                       is_essential=True,
                                       sequence=sequence,
                                       section=section)

def create_checkbox_question(content, answer_minumum, answer_maximum, sequence, section):
    return CheckBox.objects.create(question=content,
                                   is_essential=True,
                                   answer_minumum=answer_minumum,
                                   answer_maximum=answer_maximum,
                                   sequence=sequence,
                                   section=section)

def create_option(content, check_box):
    return CheckBoxOption.objects.create(option=content,
                                         check_box=check_box)

def create_file_question(question, sequence, section):
    return File.objects.create(question=question,
                               is_essential=True,
                               sequence=sequence,
                               section=section)