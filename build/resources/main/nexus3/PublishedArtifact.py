###################################################################################
#  Name: Nexus Published Artifact Trigger
#
#  Description: Trigger new release when new version of artifact is published to the Sonatype Nexus repository
#  Implementation:
#       Pull Nexus REST API to resolve an artifact identified by GAV coordinates given, and retrieve a set of details about that artifact.
#       Detected version (version and snapshotBuildNumber for snapshots) is stored into the triggerState and output variable.
#       REST API documentation: https://oss.sonatype.org/nexus-restlet1x-plugin/default/docs/path__artifact_maven_resolve.html
###################################################################################
import sys, string, urllib
import com.xhaus.jyson.JysonCodec as json

if server.serverV3:
    RESOLVE_PATH = 'service/rest/v1/search'
    RESOLVE_PARAMETERS = {
        'repository': repository,
        'maven.groupId': groupId,
        'maven.artifactId': artifactId,
        'maven.baseVersion': version
    }
else:
    RESOLVE_PATH = 'service/local/artifact/maven/resolve'
    RESOLVE_PARAMETERS = {
        'r': repositoryId,
        'g': groupId,
        'a': artifactId,
        'v': version,
        'p': packaging,
        'c': classifier,
        'e': extension
    }

if server is None:
    print "No Nexus server provided."
    sys.exit(1)

request = HttpRequest(server, username, password)
params = dict((k, v) for k, v in RESOLVE_PARAMETERS.items() if v)
context = "%s?%s" % (RESOLVE_PATH, urllib.urlencode(params))
response = request.get(context, contentType = 'application/json')

if not response.isSuccessful():
    if response.status == 404 and triggerOnInitialPublish:
        print "Artifact '%s:%s:%s' not found in repository '%s'. Ignoring." % (groupId, artifactId, version, repositoryId)
        # the following initialisation is to enable a scenario where we wish
        # to trigger a release on a first publish of an artifact to Nexus
        if not triggerState:
            artifactVersion = triggerState = '0.0.0'
    else:
        print "Failed to fetch artifact metadata from Nexus repository %s" % server['url']
        response.errorDump()
        sys.exit(1)
else:
    resolution = json.loads(response.response)
    data = resolution.get('data')

    # nexus v2 and below
    if not server.serverV3:

        version = str(data.get('version'))
        triggerState = version

        # populate output variables
        artifactVersion = version
        artifactBaseVersion = str(data.get('baseVersion')) if data.get('baseVersion') else version
        artifactSnapshotBuildNumber = str(data.get('snapshotBuildNumber')) if data.get('snapshotBuildNumber') else ''
        artifactRepositoryPath = str(data.get('repositoryPath')) if data.get('repositoryPath') else ''

    # nexus server v3
    else:

        version = str(resolution.get('items')[0].get('version')) if resolution.get('items')[0].get('version') else ''
        triggerState = version

        # populate output variables
        assetVersion = version
        assetRepository = str(resolution.get('items')[0].get('assets')[0].get('repository')) if resolution.get('items')[0].get('assets')[0].get('repository') else ''
        assetPath = str(resolution.get('items')[0].get('assets')[0].get('path')) if resolution.get('items')[0].get('assets')[0].get('path') else ''
        assetDownloadUrl = str(resolution.get('items')[0].get('assets')[0].get('downloadUrl')) if resolution.get('items')[0].get('assets')[0].get('downloadUrl') else ''
        # assetFormat = str(assets.get('format')) if assets.get('format') else ''
