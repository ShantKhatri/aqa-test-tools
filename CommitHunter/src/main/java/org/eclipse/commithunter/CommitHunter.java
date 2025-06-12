package org.eclipse.commithunter;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Map;
import java.util.HashMap;

public class CommitHunter {
    private static final Pattern OPENJ9_PATTERN = Pattern.compile("OpenJ9\\s*-\\s*([0-9a-f]+)");
    private static final Pattern OMR_PATTERN = Pattern.compile("OMR\\s*-\\s*([0-9a-f]+)");
    private static final Pattern JCL_PATTERN = Pattern.compile("JCL\\s*-\\s*([0-9a-f]+)");
    private static final Pattern JDK_VERSION_PATTERN = Pattern.compile("openjdk version \"(\\d+)\\.(\\d+)\\.(\\d+)");

    public static Map<String, String> processBuilds(String goodBuild, String badBuild) {
        Matcher goodOpenj9Matcher = OPENJ9_PATTERN.matcher(goodBuild);
        Matcher goodOmrMatcher = OMR_PATTERN.matcher(goodBuild);
        Matcher goodJclMatcher = JCL_PATTERN.matcher(goodBuild);
        Matcher goodJdkVersionMatcher = JDK_VERSION_PATTERN.matcher(goodBuild);

        if (!goodOpenj9Matcher.find() || !goodOmrMatcher.find() || !goodJclMatcher.find() || !goodJdkVersionMatcher.find()) {
            throw new IllegalArgumentException("Could not parse good build string");
        }

        Matcher badOpenj9Matcher = OPENJ9_PATTERN.matcher(badBuild);
        Matcher badOmrMatcher = OMR_PATTERN.matcher(badBuild);
        Matcher badJclMatcher = JCL_PATTERN.matcher(badBuild);

        if (!badOpenj9Matcher.find() || !badOmrMatcher.find() || !badJclMatcher.find()) {
            throw new IllegalArgumentException("Could not parse bad build string");
        }

        String jdkVersion = goodJdkVersionMatcher.group(1) + "." + goodJdkVersionMatcher.group(2);

        Map<String, String> urls = new HashMap<>();
        urls.put("openj9", String.format("https://github.com/eclipse-openj9/openj9/compare/%s...%s",
                goodOpenj9Matcher.group(1), badOpenj9Matcher.group(1)));
        urls.put("omr", String.format("https://github.com/eclipse-omr/omr/compare/%s...%s",
                goodOmrMatcher.group(1), badOmrMatcher.group(1)));
        urls.put("jcl", String.format("https://github.com/ibmruntimes/openj9-openjdk-jdk%s/compare/%s...%s",
                jdkVersion, goodJclMatcher.group(1), badJclMatcher.group(1)));

        return urls;
    }
}