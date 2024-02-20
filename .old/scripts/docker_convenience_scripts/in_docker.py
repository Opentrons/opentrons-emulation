import os

def in_container() -> bool:
    proc_1 = r"/proc/1/sched"

    if os.path.exists(proc_1):
        with open(proc_1, "r") as fp:
            out = fp.read()
    else:
        out = ""

    checks = [
        "docker" in out,
        "/lxc/" in out,
        out.split(" ")[0]
        not in (
            "systemd",
            "init",
        ),
        os.path.exists("./dockerenv"),
        os.path.exists("/.dockerinit"),
        os.getenv("container") is not None,
    ]
    return any(checks)


if __name__ == "__main__":
    print(str(in_container()).lower())
