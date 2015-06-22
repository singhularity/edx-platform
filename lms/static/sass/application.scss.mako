## Note: This Sass infrastructure is repeated in application-extend1 and application-extend2, but needed in order to address an IE9 rule limit within CSS - http://blogs.msdn.com/b/ieinternals/archive/2011/05/14/10164546.aspx

// lms - css application architecture
// ====================


// libs and resets *do not edit*
@import 'bourbon/bourbon'; // lib - bourbon
@import 'vendor/bi-app/bi-app-ltr'; // set the layout for left to right languages

// BASE  *default edX offerings*
// ====================

// base - utilities
@import 'base/reset';
% if env["FEATURES"].get("USE_CUSTOM_THEME", False):
	@import 'fonts';
	@import 'icon_fonts';
% endif
@import 'base/variables';
% if env["FEATURES"].get("USE_CUSTOM_THEME", False):
	@import 'theme-variables';
% endif
@import 'base/mixins';

@import 'base/base';

## THEMING
## -------
## Set up this file to import an edX theme library if the environment
## indicates that a theme should be used. The assumption is that the
## theme resides outside of this main edX repository, in a directory
## called themes/<theme-name>/, with its base Sass file in
## themes/<theme-name>/static/sass/_<theme-name>.scss. That one entry
## point can be used to @import in as many other things as needed.
% if env["FEATURES"].get("USE_CUSTOM_THEME", False):
  // import theme's Sass overrides
  @import '${env.get('THEME_NAME')}';
% endif

// base - assets
@import 'base/font_face';
@import 'base/extends';
@import 'base/animations';

// base - elements
@import 'elements/typography';
@import 'elements/controls';

// shared - course
@import 'shared/forms';
% if env["FEATURES"].get("USE_CUSTOM_THEME", False):
  	@import 'footer';
  	@import 'header';
	@import 'shared_course_object';
% else:
	@import 'shared/footer';
	@import 'shared/header';
	@import 'shared/course_object';
% endif
@import 'shared/course_filter';
@import 'shared/modal';
@import 'shared/activation_messages';
@import 'shared/unsubscribe';

// ONLY loading for this custom theme
% if env["FEATURES"].get("USE_CUSTOM_THEME", False):

	// shared - platform
	@import 'multicourse_home';
	@import 'multicourse_dashboard';
	@import 'multicourse/account';
	@import 'multicourse_courses';
	@import 'multicourse_course_about';
	@import 'multicourse/jobs';
	@import 'multicourse/media-kit';
	@import 'multicourse/about_pages';
	@import 'multicourse/press_release';
	@import 'multicourse/error-pages';
	@import 'multicourse/help';
	@import 'multicourse/edge';
	@import 'multicourse/survey-page';
	
	## Import styles for search
	% if env["FEATURES"].get("ENABLE_DASHBOARD_SEARCH", False):
	  @import 'search_search';
	% endif
	
	// base - specific views
	@import "views/account-settings";
	@import "views/learner-profile";
	@import 'views/login-register';
	@import 'views/verification';
	@import 'views/decoupled-verification';
	@import 'views/shoppingcart';
	@import 'views/homepage';
	@import 'course/auto-cert';
	
	// applications
	@import "discussion/utilities/variables";
	@import "discussion/mixins";
	@import 'discussion/discussion'; // Process old file after definitions but before everything else
	@import "discussion/elements/actions";
	@import "discussion/elements/editor";
	@import "discussion/elements/labels";
	@import "discussion/elements/navigation";
	@import "discussion/views/thread";
	@import "discussion/views/create-edit-post";
	@import "discussion/views/response";
	@import 'discussion/utilities/developer';
	@import 'discussion/utilities/shame';

	@import 'news';
	
% endif 

@import 'developer'; // used for any developer-created scss that needs further polish/refactoring
@import 'shame';     // used for any bad-form/orphaned scss
## NOTE: needed here for cascade and dependency purposes, but not a great permanent solution


