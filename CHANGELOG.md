### 0.8.0 (Major Release)

#### Angular UI Libraries

0.8.0 consolidates Angular UI libraries bundled with Opal. We have removed Angular Strap, and
switched all components using it to their Angular UI Bootstrap equivalents.

This is a breaking change.

Applications taking advantage of the `Forms` templatetag library should require no updates, but will see
some minor differences in visual style of widgets.

Detailed upgrade guides for the components affected (Typeahead, Popover,
Tooltip, Datepicker, Timepicker) are available in the upgrade reference documentation.

#### Defaults for Client Side subrecords

We pull through default values from subrecord fields into the Opal `Schema` and use those values when initializing the relevant
Item instance for a new subrecord. This should greatly reduce the need to use custom Angular subrecord services to set defaults.

#### Choices in form templatetags

Template tags that use the 'field' attribute to point to a subrecord field will now infer a lookup list from the Choices of the field if it exists.

Note unlike the traditional choices implementation only the last value of the choices is used and saved to the database

```python
  Colours = (
    ('P', 'Purple'),
    ('R', 'Red'),
  )
```

What is displayed to the user and saved to the database is 'Purple' or 'Red' respectively.

#### element name in template tags

The html attribute 'name' for form elements generated with the Opal `{% forms %}` templatetag library used to be inferred from the model name. Although this remains the default you can also set it with an angular expression:

```html
{% select field="Demographics.first_name" element_name="...Your Angular expression..." %}
```


#### Model removals

The models `Team`, `GP`, `CommunityNurse` and `LocatedModel` - marked for removal since 0.6.0
have now been removed.

As part of this change, the add episode modal previously available at
`/templates/modals/add_episode.html/` is now not available at the url with a trailing slash.
Any controllers attempting to open the modal e.g. custom list flows should update their
`$modal.open` call to remove the trailing slash.


#### Python 3

Opal 0.8.0 is the first version of Opal to support Python 3. This has meant changing the default
ordering of `PatientList` instances to 0 rather than None.

Moving forwards we expect all new code in Opal to be compatible with both Python 2.7 and 3.5.

This introduces an explicit Opal dependency on the Six module for maintaining codebases that span
Python 2.x and 3.x.

#### Tabbed Patient List Groups

Adds the class `opal.core.patient_lists.TabbedPatientListGroup` which displays groups of related
lists as tabs at the top of each member list.

#### Template re-naming

Modal_base has now been moved into a folder called base_templates. Its also now got a form_modal_base and a two_column_form_modal_base.
The latter two templates add validation around saving.

The standard edit item models and others now inherit from the form_modal_base.

#### Authorization and permissions

All APIs should be permissioned with Django REST framework permission classes. The default implementation uses
opal.core.api.LoginRequiredViewset, a standard DRF viewset that requires the user to be logged in.

We now require the user to be logged in for any use of the search functionality.

Added a custom interceptor that logs the user out if the we receive a 403 or 401 from the server

#### Form Validation

Adds the checkForm directive

e.g.

```html
<button check-form="form" ng-click="sendDataToTheServer">click me</button>
```

This adds default form submission behaviour to the a button. It will check if the form is valid, and if its not it will mark the button as disabled until it becomes valid.

It will also set the form as submitted.

We also now show the required error if the form has been submitted or if the field is dirty, so that the user doesn't get an ugly "fill this field in now" message when opening the modal/pathway but will get the error after they click submit.

#### Removals

Opal 0.8.0 removes a number of un-used features that have been slated for removal for some time:

* `Options` - both from the JSON API, and the Angular service.
* The legacy APIs `/api/v0.1/episode/admit` and `/api/v0.1/episode/refer`.
* The models `GP`, `CommunityNurse` and `LocatedModel`.
* `opal.models.Tagging.import_from_reversion`. This one-off classmethod on tagging was introduced to aid with the upgrade from Opal 4.x to 5.0 and has no further utility.
* The `static` argument from the forms `input` tag. Developers should move to the `static` tag.
* The _modal option to set on subrecords. This is because we now use large modals across the board.

#### Misc changes

The opal.core.api.EpisodeViewSet.create now expects tagging to be an object rather than a list, similar to how it details with demographics and location.

The API will no longer serialise the _ft or _fk_id fields of FreeTextOrForeignKey fields - these
are internal implementation details of the server that are not useful on the client side.

Adds a Unique Together constraint for (Tagging.user, Tagging.episode, Tagging.value)

Look up lists now load in from individual apps. The look for a file at {{ app }}/data/lookuplists.json

The default admin url is now `/admin/` - rather than `/admin/?` this results in more readable
admin urls and is closer to what most applications do with the Django admin.

#### Updates to the Dependency Graph

Upgrades angular to v1.5.8 (from 1.3.11) you can see their change log [here](https://github.com/angular/angular.js/blob/master/CHANGELOG.md)

Updates angular-cookies and angular-mocks to v1.5.8 (both from 1.3.11)

Updates angular-ui-select to 0.19.4 from 0.13.2

### 0.7.2 (Minor Release)

Fixes a bug with the copy to category API not setting category name.

Removes the hangover use of options in the list of teams per episode in the patient list

### 0.7.1 (Minor Release)

Completes the refactor of front end data, no longer using the `/api/v0.1/options/` API internally.
This is slated for removal in 0.8.0.

Updates DRF APIs - we now expect either Token or DjangoSession auth.

Fixes several small bugs with scaffolded applications -  the setting of `STATIC_ROOT` and
`SECRET_KEY`, generating forms for NullBooleanFields, requirements.txt.

Adds an `aligned_pair` templatetag to the `panels` library.

Updates the label for `Demographics.birth_place` to indicate that this should be a country.

Adds the `clipboard` directive to give the user one click copy to clipboard.

Adds a `tag-select` directive that renders a widget for editing the tags for an episode.

Adds metadata to the scope for patient detail views

#### Updates to the Dependency Graph

* Django Axes 1.4.0 -> 1.7.0

### 0.7.0 (Major Release)

#### Episode Categories

Refactors EpisodeCategory to be a discoverable feature.

Renames `Episode.category` -> `Episode.category_name`.

#### Episode JSON API

The Restful Episode JSON API previously available at `/episode/:pk/` is now moved into
`/api/v0.1/episode/:pk/` for consistency with the rest of our JSON APIs.
The Opal Angular layer has been updated to reflect this, and
should handle the transition seamlessly, but code calling the API directly should update
to reflect the new URL.

#### Defaults for records on the client side

Establishes a new way to define defaults for records initialized in Javascript without
requiring that we hard-code API names to defaults in a global namespace.


#### Update to Javascript Signatures

`Flow.enter()` and `Flow.exit()` now no longer take `options` positional arguments - instead
the controllers they initialize have `Metadata` and `Referencedata` as optional resolves
arguments.

AddEpisodeCtrl now no longer requires options as a resolves() option, but requires Referencedata
instead.

#### MaxLength for form helpers

The `input` form helper will now infer the max length of char fields from the max length of the
database field, and render relevant Angular directives.

#### EpisodeDetail removed

The `EpisodeDetailCtrl` and `EpisodeDetailMixin` controller and service have been removed - these
were not used anywhere other than in the Wardround plugin, and redundant after enhancements to
Patient Detail and Custom DetailViews in 0.6.

#### Additional utilities

Adds a datetimepicker templatetag that will render widgets for a Datetime field including time.

Adds a `date_of_birth_field` templatetag that renders a date of birth field complete with inteligent
validation. (Note this change also includes removing the old _partial/ template)

Updates dependency graph:

* Django -> 1.8.13

### 0.6.0 (Major Release)


**Detail views**

Moves from episode oriented detail to patient oriented detail.
(All episodes plus x-episode views are available from a patient detail screen)

**Tagging**

As a performance optimisation for the frequent access of historic tags, untagging
an episode simply renders the tag inactive rather than deleting it and relying on
Django-Reversion for access to historical data.

**Date Formatting**

We now expect 'd/m/y' date formatting by default.

**Patient lists**

Lists are now declarative, and separate from teams. They are implemented as
subclasses of opal.core.patient_lists.PatientList.

**Forms vs. Modals**

Introduces a distinction between a form and a modal.
By default, we now use forms for subrecords, only overriding the modal if there
is something we want to do differently specifically in the modal.

**Command line tools**

Adds $opal checkout for switching between applications or application versions.

### Models ContextProcessor

The 'opal.context_processors.models' Context Processor will allow you to access your
subrecords from templates without having to explicitly load them in a view. In turn,
this allows patterns like:

    {% include models.Demographics.get_detail_template %}


#### Upgrade instructions:

Full upgrade instructions to work through any backwards incompatible changes are
provided in the Opal docs.

### 0.5.5 (Minor Release)
Changes the way old tags are handled.

Tags are no longer deleted episodes, rather they're marked as archived.


### 0.5.4 (Minor Release)
* Include local storage


### 0.5.3 (Minor Release)
* Speed up loading of the lookup lists
* Fix pagination issues in search
* Speed up loading of many to many fields
* Increase test coverage
* Add some extra help fields to {% forms %} helpers
* Fixes bug with $rootScope.open_modal() where keystrokes were being intercepted

### 0.5.2 (Minor Release)
Speed improvements on page load
allow us to only show record panels if a record of that type exists
disable modal buttons while saving


### 0.5.1 (Minor Release)
Minor bug fixes


### 0.5 (Major release)

**Search**

Complete re-design of Search interface to provide a single search box on every page and pagination for resulta.
Puts in place a pluggable interface that could be swapped out for e.g. ElasticSearch.
New Service for PatientSummary()

**Analytics**

Moves Analytics integration into Opal core with the ability to blacklist pages that should never be reported

**List view**

Removed old spreadsheet-style cell based navigation and moved to row-wise nav with clearer highlighting of the active row.
Updated scrolling and loading behaviour to snap to viewport and not display the page build.

**Subrecord metadata**

Added four new utility fields to Patient and Episode subrecords:

created_by, updated_by, created, updated

**Select2 and list fields**

Added support for select2 as an input widget and Subrecord fields that can be lists of things.

**Also**

Numerous small bugfixes.
Refactoring of the models package into a models module.
Updated Underscore.js -> 1.8.3
Updated Angular.js -> 1.3.11

### 0.4.3 (Minor release)

Refactors opal.models to be a models.py file rather than a package.
Adds several improvements to forms helpers -> Help argument, other argument to select.

Updates dependency graph:

* Angular-strap -> 2.3.1

### 0.4.2 (Minor release)

Upgrades dependency graph:

* Django -> 1.8.3
* Django-reversion -> 1.8.7
* jQuery -> 1.11.3
* D3 -> 3.5.6
* C4 -> 0.4.10

South has been removed, now using django migrations

### 0.4.1 (Bugfix release)

Fixes some search results appearing duplicated.

### 0.4 (Major release)

**New Design**

Completely re-designed UI following extensive user research and multiple iterations.

**Managementcommands and scaffolding**

Features the opal command line tool for common administrative tasks
http://opal.openhealthcare.org.uk/docs/guides/command_line_tool/

** Form helpers templatetag library**

New template library for consistent form controls in line with our new interface guidelines
http://opal.openhealthcare.org.uk/docs/reference/form_templatetags/

**API Documentation**


Opal JSON APIs are now fully self-documenting for all updated instances
http://opal.openhealthcare.org.uk/docs/guides/json_api/

### 0.3 (Major release)

Bugfixes, significant flexibility in template customisability.

Minor UI updates.

### 0.2.2 (Bugfix release)

Numerous small bugfixes.

Adds the concept of undischarging patients.

### 0.2.1

Numerous small bugfixes.


### 0.2.0

Search overhaul - introduces advanced searches.

### 0.1.1

Initial public release
