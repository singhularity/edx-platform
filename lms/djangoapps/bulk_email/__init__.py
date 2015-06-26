from models import CourseEmailTemplate

def initialize_template():

    defaultTemplate = CourseEmailTemplate(html_template = "{{message_body}}",
                                          plain_template = "{{message_body}}",
                                          name = "amplifyDefaultTemplate")

    defaultTemplate.save(force_insert=True)

if CourseEmailTemplate.objects.filter(name='amplifyDefaultTemplate').count() == 0:
    initialize_template()
