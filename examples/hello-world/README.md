# Hello World

A dependency-free `fetch-js` app for the Apps Platform. Its handler returns a
small HTML page at `/` and a 404 for other paths. Building the artifact requires
Python 3; deploying requires the `bl` binary and an Apps control-plane URL.

From the repository root, choose an available app ID and use the same version
ID when building and deploying:

```sh
python3 examples/hello-world/build.py \
  --app-id my-hello-world \
  --version-id hello-world-v1 \
  --output /tmp/hello-world-artifact.tar.gz

target/release/bl --json apps create \
  --app-id my-hello-world --runtime-profile fetch-js --persistence none

target/release/bl --json apps deploy my-hello-world \
  /tmp/hello-world-artifact.tar.gz --version-id hello-world-v1

target/release/bl --json apps ready my-hello-world \
  --version-id hello-world-v1
```

Use `BL_APPS_CONTROL_PLANE_URL` or `--base-url` to select the control plane.
On Blox, its configured origin uses workstation authentication. Other approved
ingress URLs require `bl auth login` and organization configuration.

The deploy response supplies the site URL. Poll `apps ready` until that exact
version is ready, then open the URL. Viewer access follows the app's access
policy; use `bl apps access get my-hello-world` to inspect it.
