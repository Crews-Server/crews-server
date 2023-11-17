"""
테스트를 위한 CONSTANT
"""


'''
모집 공고 생성 요청
'''
POST_REQUEST = {"apply_start_date": "2023-09-20 00:00:00",
                "apply_end_date": "2023-09-22 00:00:00",
                "document_result_date": "2023-09-23 00:00:00",
                "has_interview": "true",
                "interview_start_date": "2023-10-01 00:00:00",
                "interview_end_date": "2023-10-02 00:00:00",
                "final_result_date": "2023-10-03 00:00:00",
                "requirement_target": "열정 있는 미래 창업인들",
                "title": "서강대학교 멋쟁이사자처럼 12기에서 신입 부원을 모집합니다!",
                "content": "OT 필참이며 날짜는 23년 10월 10일입니다!",
                "membership_fee": "1년 활동 기간 동안 동아리에서 사용할 6만원",
                "crew": 1,
                "progress": "1차는 서류, 2차는 비대면(Zoom) 면접"}


'''
잘못된 모집 공고 생성 요청
- content가 없어서 validation 문제가 발생한다
- 1차 전형만 있어서 면접 일정이 입력되지 않는다
'''
BAD_POST_REQUEST = {"apply_start_date": "2023-09-20 00:00:00",
                    "apply_end_date": "2023-09-22 00:00:00",
                    "document_result_date": "2023-09-23 00:00:00",
                    "has_interview": "false",
                    "requirement_target": "열정 있는 미래 창업인들",
                    "title": "서강대학교 멋쟁이사자처럼 12기에서 신입 부원을 모집합니다!",
                    "membership_fee": "1년 활동 기간 동안 동아리에서 사용할 6만원",
                    "crew": 1,
                    "progress": "1차 서류만 진행합니다."}


'''
상시 모집 공고 생성 요청
- apply_end_date와 document_result_date가 항상 '9999-12-31 23:59:59.999999'이다.
'''
ON_GOING_POST_REQUEST = {"apply_start_date": "2023-09-20 00:00:00",
                         "apply_end_date": "9999-12-31 23:59:59.999999",
                         "document_result_date": "9999-12-31 23:59:59.999999",
                         "has_interview": "false",
                         "requirement_target": "열정 있는 미래 창업인들",
                         "title": "서강대학교 멋쟁이사자처럼 12기에서 신입 부원을 모집합니다!",
                         "content": "마구마구지원부탁요",
                         "membership_fee": "1년 활동 기간 동안 동아리에서 사용할 6만원",
                         "crew": 1,
                         "progress": "1차 서류만 진행합니다."}


'''
지원서 중 장문형 문항 생성 요청
'''
LONG_SENTENCE_CREATE_REQUEST = {
    "post_id": 1,
    "section_name": "공통",
    "description": "모든 사람이 답변해야 하는 공통 문항입니다.",
    "question":
    [
        {
            "type": "long_sentence",
            "is_essential": True,
            "question": "자기소개하세요.",
            "letter_count_limit": 300
        },
        {
            "type": "long_sentence",
            "is_essential": True,
            "question": "지원 동기를 적어주세요.",
            "letter_count_limit": 500
        }
    ]
}

'''
지원서 중 객관식 & 파일 문항 생성 요청
'''
CHECKBOX_FILE_CREATE_REQUEST = {
    "post_id": 1,
    "section_name": "공통",
    "description": "모든 사람이 답변해야 하는 공통 문항입니다.",
    "question":
    [
        {
            "type": "checkbox",
            "is_essential": True,
            "question": "옵션 중 하나를 선택하세요.",
            "answer_minumum": 1,
            "answer_maximum": 1,
            "options": ['옵션 1', '옵션 2', '옵션 3']
        },
        {
            "type": "file",
            "is_essential": True,
            "question": "포트폴리오 파일을 첨부해주세요."
        }
    ]
}