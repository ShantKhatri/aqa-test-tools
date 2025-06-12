package org.eclipse.commithunter;

import java.util.Map;

public class CommitHunterCLI {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Usage: java -jar commit-hunter.jar <good_build_string> <bad_build_string>");
            System.exit(1);
        }

        try {
            String goodBuild = args[0].replace("\\n", "\n");
            String badBuild = args[1].replace("\\n", "\n");

            Map<String, String> urls = CommitHunter.processBuilds(goodBuild, badBuild);

            System.out.println("OpenJ9: " + urls.get("openj9"));
            System.out.println("OMR: " + urls.get("omr"));
            System.out.println("JCL: " + urls.get("jcl"));
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}