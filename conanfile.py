import os
from conans import ConanFile, CMake, tools

class QtrendererConan(ConanFile):
    name = "qtrenderer"
    version = "11.2.2"
    license = "https://www.mesa3d.org/license.html"
    author = "Mathias Eggert mathias.eggert@nexenio.com"
    url = "https://download.qt.io/development_releases/prebuilt/llvmpipe/windows"
    description = "Conan.io package for the Software Renderer of the Qt library. Is needed under windows as fallback, if no graphic driver is workingfor qt."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        if self.settings.os != "Windows":
            print("only available under windows -> package script is do nothing on other platforms")
            return

        # download software renderer
        if self.settings.arch == "x86_64":
            sw_url = 'https://download.qt.io/development_releases/prebuilt/llvmpipe/windows/opengl32sw-64-mesa_11_2_2.7z'
            sha256 = '142A74BFBE7D2B1BF633925F130B29EB10FFA9FB87CC1BBD05EE2624EE81D261'
        else:
            sw_url = 'https://download.qt.io/development_releases/prebuilt/llvmpipe/windows/opengl32sw-32-mesa_11_2_2.7z'
            sha256 = '9BF62DB2F222329DE5F75578239BF203553884FB9417D8E4FF89D1CACE9A6535'

        sw_filename = os.path.basename(sw_url)
        tools.download(sw_url, sw_filename)
        tools.check_sha256(sw_filename, sha256)

        os.rename(sw_filename, self.name)

    def build(self):
        # unpack software renderer
        self.run("cmake -E tar xzf %s" % (self.name));

    def package(self):
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["qtrenderer"]

