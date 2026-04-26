### Testing Methodology

The purpose of this document is to describe and elaborate on the testing methodology that is to occur (or rather that has occured).

---

The primary goal for testing is to be able to provide a stable and working build that can later be added onto with confidence in knowing that the code is;
functioning and error free.

With this in mind, the vast majority of the testing, based on the features that are in the works; will have to undergo
testing via running the application and checking for any breakages or failure points.

While there are some unit tests for specific items such as token generation for admin access, email notifications, and date utilities.
The further we go along, the more functional tests will be conducted and potentially more unit tests will be added.
As it stands, the following procedure goes as follows:

- Receive pull request.
- Either copy the code and structure or switch to that branch.
- Test the code on the main branch.
- Approve.
- Test with all others and their versions once all items are approved.

---

As programmers, knowing at first that the code does work is important, this way we can see what it is supposed to do.
Which makes life easier when there are conflicts and breakages, since patches will have to go up in order to correct the conflict.

