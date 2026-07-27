<?php
// Report the values a Moodle SCORM attempt has stored.

define('CLI_SCRIPT', true);

$options = getopt('', ['config:', 'scormid:', 'userid:', 'attempt:']);
foreach (['config', 'scormid', 'userid'] as $required) {
    if (empty($options[$required])) {
        fwrite(STDERR, "Missing required option --{$required}\n");
        exit(2);
    }
}

$config = realpath($options['config']);
if ($config === false) {
    fwrite(STDERR, "Config path does not exist\n");
    exit(2);
}

require($config);
require_once($CFG->libdir . '/gradelib.php');

$scormid = (int)$options['scormid'];
$userid = (int)$options['userid'];
$attempt = isset($options['attempt']) ? (int)$options['attempt'] : 1;
$scorm = $DB->get_record('scorm', ['id' => $scormid], '*', MUST_EXIST);
$user = $DB->get_record('user', ['id' => $userid], '*', MUST_EXIST);

$tracks = [];
$dbmanager = $DB->get_manager();
if ($dbmanager->table_exists(new xmldb_table('scorm_scoes_track'))) {
    $records = $DB->get_records(
        'scorm_scoes_track',
        [
            'scormid' => $scormid,
            'userid' => $userid,
            'attempt' => $attempt,
        ],
        'element ASC'
    );
    foreach ($records as $record) {
        $tracks[$record->element] = $record->value;
    }
} else {
    $sql = "SELECT v.id, s.identifier, e.element, v.value, v.timemodified
              FROM {scorm_scoes_value} v
              JOIN {scorm_scoes} s ON s.id = v.scoid
              JOIN {scorm_attempt} a ON a.id = v.attemptid
              JOIN {scorm_element} e ON e.id = v.elementid
             WHERE s.scorm = :scormid
               AND a.scormid = :attemptscormid
               AND a.userid = :userid
               AND a.attempt = :attempt
          ORDER BY s.identifier, e.element";
    $records = $DB->get_records_sql($sql, [
        'scormid' => $scormid,
        'attemptscormid' => $scormid,
        'userid' => $userid,
        'attempt' => $attempt,
    ]);
    foreach ($records as $record) {
        $tracks[$record->identifier . ':' . $record->element] = $record->value;
    }
}

$grades = grade_get_grades($scorm->course, 'mod', 'scorm', $scormid, $userid);
$grade = $grades->items[0]->grades[$userid] ?? null;

echo json_encode([
    'scormid' => $scormid,
    'userid' => $userid,
    'user' => fullname($user),
    'attempt' => $attempt,
    'tracks' => $tracks,
    'grade' => $grade ? [
        'grade' => $grade->grade,
        'str_grade' => $grade->str_grade,
        'feedback' => $grade->feedback,
    ] : null,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;
