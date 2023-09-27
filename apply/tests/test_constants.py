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
