 SaltStack Boto3 Project
=======================

This is a friendly-fork of the [SaltStack][] repository for the purpose of
reworking the [AWS][] [Boto][] portions of the code to use [Boto3][].  While
this repository is kept in-sync with the up-stream [SaltStack][] repository, it
is not intended as a general-use repository outside of the scope of
refactoring/testing the [AWS][] [Boto3][] modules/states.

About Boto
----------

> [Boto][] is the [Amazon Web Service][AWS]([AWS][])
> [Software Development Kit][SDK]([SDK][]) for [Python][], which allows [Python][]
> developers to write software that makes use of services like [Amazon S3][S3]
> and [Amazon EC2][EC2]. You can find the latest, most up to date,
> documentation at our doc site, including a list of services that are
> supported.

[Boto v2.49.0][Boto] was released on July of 2018.  This was the final
maintenance release of the [Boto v2][Boto] SDK.  The first commit of the new
[Boto3][] [SDK][] was made in September of 2014 with version _1.0.0_ being
released in June of 2015.

During development of the 3rd version of the [Boto][] [SDK][], a decision was
made to call this [Python][] library [Boto3][]. Pressumably this was done to
allow the simultanous `import` of both [Boto v2][Boto] and [Boto v3][Boto3] for
development/testing purposes.

For unknown reasons, when [Boto v3][Boto3] was finally released, the
development team chose to maintain the [Boto3][] naming convention. This
created a situation where applications, including [SaltStack][], were
desincentivized to work through the process of upgrading their code to work
with [Boto v3][Boto3] (as would normally be the case had the [Boto3][] team
chosen to release the library as [Boto v3.0.0][Boto3]).

At this time the [Boto v2][Boto] code has been end-of-life since 2018 while
[Boto v3][Boto3] has been in common usage since 2015. This project aims to
replace [Boto v2][Boto] usage in [SaltStack][] with [Boto3][].

What about Idem?
----------------

[Idem][] is a sort of replacement/co-routine/parallel development project
started by [SaltStack][] that is built atop [POP][]. [SaltStack][] itself has
support for calling out to [Idem][] with the basic idea being that
[SaltStack][] keeps its job as an orchestration tool and [Idem][] is used to
handle state management/changes.

While [Idem][] makes a wide variety of promises/claims to usability/simplicity,
thus far it is not a usable solution, and it does not appear that it will be
usable in the near-future. Further more, there are a number of development
choices made within some [Idem][] subsystems (such as the [Idem AWS][]) that
make it uncertain if it will in fact be usable for managing [AWS][]
infrastructure any time soon.

1. By default [Idem AWS][] does not work with the default [AWS][] config.
   [Idem AWS][] requires pre-configured [AWS][] Keys/Secrets.  This is in
   contrast with standard practice within [Boto3][] and the
   [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/) which have well
   defined default configuration behavior.  The existing standard is to obey
   any existing
   [AWS configurations](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html),
   or to use existing instance credentials assigned to the [EC2][] or [ECS][]
   instance the call is made from.  [Idem AWS][] has chosen to deviate from
   accepted practices and place extra (and unnecessary) configuration burdens
   on the user.
2. [Idem AWS][] is directly implmenting functionality normally found within
   [Salt Cloud][] This appears to be a duplication of work when one considers
   that there is already an existing
   [Idem Cloud](https://github.com/saltstack/idem-cloud) project.  It is not
   clear if there is some deficiency within [Idem][] that has resulted in this
   duplication of work, or if it highlights some flaw with the [POP][] model.
3. [Idem AWS][] is quite restrictive on its assumed use case, so much so that
   it is incapable of handling many default [AWS][] resources such as the
   default [VPC][].
4. Development on [Idem AWS][] changed direction in which an `idem-boto3`
   subsystem (source location unknown) was created that [Idem AWS][] will be
   rewritten to use.  This is very much the same model that [SaltStack][] is
   already using with the existing [Boto3][] code, and once again raises the
   concern as to what problem [Idem][] or [POP][] is actually solving.

At this time great deal of development within [SaltStack][] has stalled as
developers/users wait to see the status of [Idem][].

> Dec 18 2020 #idem-cloud:
> Question... we are looking to start a big refactor on our salt-cloud profiles
> to try to de-duplicate some of it.   But if idem-aws is coming soon we will
> just wait.   Thoughts on if we should wait, or spend the time now on
> something that will be replaced (hopefully soon)?

These concerns and others have been raised in chat channels and issues/bugs
opened within the [Idem AWS](https://gitlab.com/saltstack/pop/idem-aws/)
project yet have not been acknowledged by the project developers.

As there is no release schedule/timeline/roadmap/communication coming
from the [Idem AWS][] team, and as there is no clear indication as to what in
[Idem AWS][] is improved over traditional [Saltstack][] (outside of the _shiny_
factor), we have chosen to not wait further.

Existing code and existing infrastructure need maintenance, and at current
[Idem AWS][] is not a usable solution.

Boto plans
----------

During the rewrite **all** [Boto v2][Boto] modules/states will be marked as deprecated.

Most (though not all) of the [Boto v2][Boto] [SaltStack][] modules are prefixed
with `boto_`. Curiously, _some_ of these modules include [Boto3][] code in
order to work-around deficiencies in [Boto v2][Boto].

```
    try:
        # Using conn.get_response is a bit of a hack, but it avoids having to
        # rewrite this whole module based on boto3
        for ret in __utils__["boto.paged_call"](
            conn.get_response,
            "ListAttachedUserPolicies",
            params,
            list_marker="AttachedPolicies",
        ):
            policies.extend(
                ret.get("list_attached_user_policies_response", {})
                .get("list_attached_user_policies_result", {})
                .get("attached_policies", [])
            )
        return policies
```

Boto3
-----

As a general convention, most [SaltStack][] modules/states are named
`boto3_<iface>`, unfortunately this is not always true.  A number of interfaces
which are [Boto3][] are named as `boto_*`, which greatly confuses the
situation. All [Boto3][] interfaces will be renamed to be prefixed with
`boto3_`. Place-holder interfaces will be inserted into the code under the
old-names which include a deprecation warning, but which otherwise call the new
interface.

Non-Boto AWS code
-----------------

There are a number of other interfaces in [SaltStack][] which attempt to
implement restful interfaces for managing [AWS][] resources (E.g. the
[salt S3 module](https://docs.saltproject.io/en/latest/ref/modules/all/salt.modules.s3.html)).
These interfaces duplicate the functionality of [Boto3][] and are no longer
maintained.  All of these interfaces will be marked as deprecated.

Contributing
------------

This project utilizes [Git Assembler][] to manage the `master` branch.  This
means that `master` branch _will_ be rebased regularly.  Due to this,
development of code should never be performed against this projects `master`.
All topic branches should be based against the upstream [SaltStack][] master.

[Git][] config example:

```
[pull]
	rebase = true
[remote "origin"]
        url = https://github.com/saltstack/salt.git
        pushurl = ssh://git@github.com/example/salt.git
        gh-resolved = base
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
        remote = origin
        merge = refs/heads/master
        rebase = false
```

Changes for a module should exist in isolation on their own topic branch:

```
feat/boto_deprecate_ec2 origin/master
feat/boto_deprecate_elasticache origin/master
feat/boto_deprecate_route53 origin/master
feat/boto_deprecate_sns origin/master
feat/boto3_refactor_s3 origin/master
misc/boto3_project origin/master
```

_note: `origin` in this context is the [SaltStack][] `origin`_

It will be the job of [Git Assembler][] to update `master` from all
[Boto][]/[Boto3][] branches and regenerate release tags against upstream
[SaltStack][] releases which include changes introduced from the above topic
branches.

All changes to the [Git Assembler][] [assembly file](.git-assembly) should be
made on the `misc/boto3_project` branch and `git fetch --all` should always be
run before running [Git Assembler][]. _note: it is recommended that you create
a symlink from `.git/assembly` to the `.git-assembly` file located in the
topdir._

Pull-requests and issues should be submitted against each topic branch and not
against the `master`.

[//]: # (The following are reference links used elsewhere in the document)

[AWS]: https://aws.amazon.com
[Boto]: https://github.com/boto/boto
[Boto3]: https://github.com/boto/boto3
[EC2]: https://aws.amazon.com/ec2
[ECS]: https://aws.amazon.com/ecs
[Git]: https://git-scm.com
[Git Assembler]: https://www.thregr.org/~wavexx/software/git-assembler/
[GitHub]: https://github.com
[Idem]: https://gitlab.com/saltstack/pop/idem
[Idem AWS]: https://gitlab.com/saltstack/pop/idem-aws
[POP]: https://pypi.org/project/pop
[Python]: https://www.python.org
[S3]: https://aws.amazon.com/s3
[SaltStack]: https://github.com/saltstack/salt
[Salt Cloud]: https://docs.saltproject.io/en/latest/topics/cloud
[SDK]: https://en.wikipedia.org/wiki/Software_development_kit
[VPC]: https://aws.amazon.com/vpc
