var app = angular.module('opal');

app.config(
    ['$routeProvider',
     function($routeProvider) {
             $routeProvider.when('/list/',{
                controller: 'EpisodeRedirectListCtrl',
                templateUrl: '/templates/episode_list.html',
             }).when('/list/:slug', {
			     controller: 'EpisodeListCtrl',
			     resolve: {
				     episodes: function(episodesLoader, $route) {
               return episodesLoader($route.current.params.slug);
             },
				     options: function(Options) { return Options; },
             menuItems: function(patientListLoader){ return patientListLoader(); },
             profile: function(UserProfile){ return UserProfile; },
             episodeVisibility: function(episodeVisibility){
                 return episodeVisibility;
             }
             profile: function(UserProfile){ return UserProfile; },
			     },
			     templateUrl: function(params){
                     var target =  '/templates/episode_list.html';
                     if(params.tag){
                         target += '/' + params.tag;
                         if(params.subtag){
                             target += '-' + params.subtag;
                         }
                     }
                     return target;
                 }
		     })
             .when('/patient/:patient_id/:view?', {
			     controller: 'PatientDetailCtrl',
                 resolve: {
				     patient: function(patientLoader) { return patientLoader(); },
				     options: function(Options) { return Options; },
                     profile: function(UserProfile){ return UserProfile; }
                 },
			     templateUrl: function(params){ return '/templates/patient_detail.html' }
             })
             .when('/search', {
			     controller: 'SearchCtrl',
			     templateUrl: '/search/templates/search.html',
             })
             .when('/extract', {
                 controller: 'ExtractCtrl',
                 templateUrl: '/search/templates/extract.html',
                 resolve: {
                     profile: function(UserProfile){ return UserProfile; },
                     schema: function(extractSchemaLoader){ return extractSchemaLoader; },
				     options: function(Options) { return Options; },
                     filters: function(filtersLoader){ return filtersLoader(); }
                 }
             })
             .when('/account', {
                 controller: 'AccountCtrl',
                 templateUrl: '/accounts/templates/account_detail.html'
		     })
             .otherwise({redirectTo: '/'});
     }]);
