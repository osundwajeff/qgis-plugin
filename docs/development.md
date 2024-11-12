## Documentation about installation and development setup
### 📚 Versions

* Available and supported in all the QGIS 3.x versions

| Plugin version(s)                                                                                                                                                                                                                         | Minimum QGIS version | Maximum QGIS version |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|----------------------|
| ![GitHub Epic 1 Release)](https://img.shields.io/github/v/release/earthdaily/qgis-plugin?logo=semanticrelease&label=latest-release)<br> ![](https://img.shields.io/badge/stable_version-v0.0.1-blue?logo=semanticrelease) | 3.10                 | 3.26                 |


### ⚙️ Installation

During the development phase the plugin is available to install via
a dedicated plugin repository 

[https://raw.githubusercontent.com/earthdaily/qgis-plugin/release/docs/repository/plugins.xml](https://raw.githubusercontent.com/earthdaily/qgis-plugin/release/docs/repository/plugins.xml)

[//]: # ()
[//]: # (#### Install from QGIS plugin repository)

[//]: # ()
[//]: # (- Open QGIS application and open plugin manager.)

[//]: # (- Search for `EarthDaily` in the All page of the plugin manager.)

[//]: # (- From the found results, click on the `EarthDaily` result item and a page with plugin information will show up. )

[//]: # (  )
[//]: # (- Click the `Install Plugin` button at the bottom of the dialog to install the plugin.)

[//]: # ()

#### Install from ZIP file

Alternatively the plugin can be installed using **Install from ZIP** option on the 
QGIS plugin manager.

- Download zip file from the required plugin released version
https://github.com/earthdaily/qgis-plugin/releases/download/{tagname}/geosys.{version}.zip or create one
using the admin interface as explained [here](https://github.com/earthdaily/qgis-plugin#plugin-admin-interface).

- From the **Install from ZIP** page, select the zip file and click the **Install** button to install plugin.

#### Install from custom plugin repository


- Open the QGIS plugin manager, then select the **Settings** page

- Click **Add** button on the **Plugin Repositories** group box and use the above url to create the new plugin repository.

- The plugin should now be available from the list of all plugins that can be installed.

Disable QGIS official plugin repository in order to not fetch plugins from it.

**NOTE:** While the development phase is on going the plugin will be flagged as experimental, make
sure to enable the QGIS plugin manager in the **Settings** page to show the experimental plugins
in order to be able to install it.

When the development work is complete the plugin will be available on the QGIS
official plugin [repository](https://plugins.qgis.org/plugins).


### 🛠️ Development 

To use the plugin for development purposes, clone the repository locally,
install pip, a python dependencies management tool, see https://pypi.org/project/pip/.


#### Create virtual environment

Using any python virtual environment manager create project environment. 
Recommending to use [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

It can be installed using python pip 

```
pip install virtualenvwrapper
```

 1. Create virtual environment

    ```
    mkvirtualenv geosys
    ```

2. Using the pip, install plugin development dependencies by running 

    ```
    pip install -r requirements-dev.txt
    ```

3. Install an automatic code formatting hook using the following command, 
   this will run code style checks each time a commit is created.
    ```
    pre-commit install
    ```
   Run the following pre-commit command after installing the pre-commit hook
   for the first time.
   ```
    pre-commit run --all-files
   ```

#### Plugin admin interface
The plugin contains a script that can be used for various development tasks.

Generate a plugin zip file using the below command, after a successful run the plugin zip file will be located
on the `dist` folder under the plugin root folder.

```
python admin.py generate-zip
```

### 🔧 Testing

The plugin currently support running tests on Linux environment only, to run plugin tests use the below script
from the plugin root.
```
   ./run-docker-tests.sh
```

The script builds a testable plugin code and then it spins up Docker containers that contain QGIS version 3.10 and 3.26 
 images respectively, finally it runs the available test suite. Python is required to
be installed in the system before using the script.

When using the script for the first time it will pull the QGIS Docker images if there are not available 
locally. After the tests have finished running the Docker containers created for the tests will be stopped and removed.


### 📃 Documentation

The plugin documentation page is available at https://github.com/earthdaily/qgis-plugin
