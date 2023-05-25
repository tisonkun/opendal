package org.apache.opendal;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

public final class NativeLoader {
    public static final String LIBNAME = "opendaljni";

    private static final String OS = System.getProperty("os.name").toLowerCase();
    private static final String ARCH = System.getProperty("os.arch").toLowerCase();

    public static boolean isWindows() {
        return OS.contains("win");
    }
    public static boolean isMac() {
        return OS.contains("mac");
    }
    public static boolean isUnix() {
        return OS.contains("nix") || OS.contains("nux");
    }

    public static void loadLibrary(String name) {
        final String path = String.format("/native/%s", getJniLibraryFileName(name));

        try (final InputStream is = NativeLoader.class.getResourceAsStream(path)) {
            if (is == null) {
                throw new UnsatisfiedLinkError("cannot load library " + name);
            }

            final File tmpfile = File.createTempFile(path, null);
            tmpfile.deleteOnExit();

            Files.copy(is, tmpfile.toPath(), StandardCopyOption.REPLACE_EXISTING);
            System.load(tmpfile.getAbsolutePath());
        } catch (IOException e) {
            throw new UncheckedIOException("cannot load library " + name, e);
        }
    }

    public static String getJniLibraryFileName(String name) {
        String arch = ARCH;
        if (arch.equals("amd64")) {
            arch = "x86_64";
        } else if (arch.equals("arm64")) {
            arch = "aarch64";
        }

        if (isUnix()) {
            return String.format("lib%s-linux-%s.so", name, arch);
        } else if (isMac()) {
            return String.format("lib%s-osx-%s.dylib", name, arch);
        } else if (isWindows()) {
            return String.format("lib%s-win-%s.dll", name, arch);
        }
        throw new UnsupportedOperationException("Unsupported platform " + OS + "@" + arch);
    }
}
