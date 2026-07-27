<?php
// Import a SCORM package into a disposable Moodle course from the command line.

define('CLI_SCRIPT', true);

$options = getopt('', ['config:', 'courseid:', 'package:', 'name:']);
foreach (['config', 'courseid', 'package', 'name'] as $required) {
    if (empty($options[$required])) {
        fwrite(STDERR, "Missing required option --{$required}\n");
        exit(2);
    }
}

$config = realpath($options['config']);
$package = realpath($options['package']);
if ($config === false || $package === false) {
    fwrite(STDERR, "Config or package path does not exist\n");
    exit(2);
}

require($config);
require_once($CFG->libdir . '/clilib.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->dirroot . '/mod/scorm/lib.php');
require_once($CFG->dirroot . '/mod/scorm/locallib.php');

$admin = get_admin();
\core\session\manager::set_user($admin);

$courseid = (int)$options['courseid'];
$course = get_course($courseid);
$name = trim($options['name']);

$module = $DB->get_record('modules', ['name' => 'scorm'], '*', MUST_EXIST);
$existing = $DB->get_record('scorm', ['course' => $courseid, 'name' => $name]);
if ($existing) {
    $cm = get_coursemodule_from_instance('scorm', $existing->id, $courseid, false, MUST_EXIST);
    echo json_encode([
        'status' => 'already_exists',
        'courseid' => $courseid,
        'scormid' => $existing->id,
        'cmid' => $cm->id,
        'version' => $existing->version,
        'reference' => $existing->reference,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;
    exit(0);
}

$draftitemid = file_get_unused_draft_itemid();
$usercontext = context_user::instance($admin->id);
$fs = get_file_storage();
$filename = basename($package);
$fs->create_file_from_pathname([
    'contextid' => $usercontext->id,
    'component' => 'user',
    'filearea' => 'draft',
    'itemid' => $draftitemid,
    'filepath' => '/',
    'filename' => $filename,
    'userid' => $admin->id,
    'author' => fullname($admin),
], $package);

[, , , , $moduleinfo] = prepare_new_moduleinfo_data($course, 'scorm', 0);
$moduleinfo->name = $name;
$moduleinfo->module = $module->id;
$moduleinfo->modulename = 'scorm';
$moduleinfo->section = 0;
$moduleinfo->beforemod = 0;
$moduleinfo->cmidnumber = '';
$moduleinfo->visible = 1;
$moduleinfo->visibleoncoursepage = 1;
$moduleinfo->showdescription = 0;
$moduleinfo->introeditor = [
    'text' => 'Moodle 5.2 compatibility test for the commercial SCORM package.',
    'format' => FORMAT_HTML,
    'itemid' => file_get_unused_draft_itemid(),
];

$moduleinfo->scormtype = SCORM_TYPE_LOCAL;
$moduleinfo->packagefile = $draftitemid;
$moduleinfo->reference = '';
$moduleinfo->version = '';
$moduleinfo->maxgrade = 100;
$moduleinfo->grademethod = GRADEHIGHEST;
$moduleinfo->whatgrade = 0;
$moduleinfo->maxattempt = 0;
$moduleinfo->forcecompleted = 0;
$moduleinfo->forcenewattempt = 0;
$moduleinfo->lastattemptlock = 0;
$moduleinfo->masteryoverride = 1;
$moduleinfo->displayattemptstatus = 1;
$moduleinfo->displaycoursestructure = 0;
$moduleinfo->updatefreq = 0;
$moduleinfo->sha1hash = null;
$moduleinfo->md5hash = '';
$moduleinfo->revision = 0;
$moduleinfo->launch = 0;
$moduleinfo->skipview = 2;
$moduleinfo->hidebrowse = 0;
$moduleinfo->hidetoc = SCORM_TOC_DISABLED;
$moduleinfo->nav = SCORM_NAV_DISABLED;
$moduleinfo->navpositionleft = -100;
$moduleinfo->navpositiontop = -100;
$moduleinfo->auto = 0;
$moduleinfo->autocommit = 1;
$moduleinfo->popup = 0;
$moduleinfo->width = 100;
$moduleinfo->height = 800;
$moduleinfo->timeopen = 0;
$moduleinfo->timeclose = 0;
$moduleinfo->timemodified = time();
$moduleinfo->completionstatusallscos = 0;

$created = add_moduleinfo($moduleinfo, $course);
$scorm = $DB->get_record('scorm', ['id' => $created->instance], '*', MUST_EXIST);
$scoes = $DB->get_records('scorm_scoes', ['scorm' => $scorm->id], 'sortorder ASC');
$launchables = array_values(array_filter($scoes, static fn($sco) => !empty($sco->launch)));

echo json_encode([
    'status' => 'imported',
    'courseid' => $courseid,
    'scormid' => $scorm->id,
    'cmid' => $created->coursemodule,
    'version' => $scorm->version,
    'reference' => $scorm->reference,
    'scoes' => count($scoes),
    'launchable_scoes' => count($launchables),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;
