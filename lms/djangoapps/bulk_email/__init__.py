from models import CourseEmailTemplate

# This section of code creates a default CourseEmailTemplate in the django admin console
# Bulk email must have a template in order to be sent. Here we create a basic default template
# the first time an instance is set up. The end of the code checks to make sure that the template
# doesn't already exist, so the template only gets added the very first time.

def initialize_template():

    defaultTemplate = CourseEmailTemplate(html_template = "{{message_body}}",
                                          plain_template = "{{message_body}}",
                                          name = "amplifyDefaultTemplate")

    defaultTemplate.save(force_insert=True)

if CourseEmailTemplate.objects.filter(name='amplifyDefaultTemplate').count() == 0:
    initialize_template()
