from datetime import datetime

from table.models import Post, Crew, Category


def create_post(id, apply_end_date, title, crew):
    return Post.objects.create(
        id=id,
        apply_start_date="1000-01-01 00:00:00",
        apply_end_date=parse_end_date(apply_end_date),
        document_result_date="1000-01-01 00:00:00",
        has_interview=False,
        requirement_target="0",
        title=title,
        content="0",
        membership_fee="0",
        crew=crew,
        progress="0"
    )

def parse_end_date(apply_end_date):
    if apply_end_date == datetime.max:
        return apply_end_date.strftime('%Y-%m-%d %H:%M:%S.%f')
    return apply_end_date.strftime('%Y-%m-%d 00:00:00')

def create_category(id, name):
    return Category.objects.create(id=id, category_name=name)

def create_crew(id, name, category):
    return Crew.objects.create(id=id, crew_name=name, description="0", category = category)