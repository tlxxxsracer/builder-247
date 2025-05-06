import { Router, RequestHandler } from "express";
import { verifyBearerToken } from "../middleware/auth";
import { validateSignature, getSignatureGenerationDocs } from "../middleware/signature_validation";

/******** Existing Imports... **********/

const router = Router();

// Add a documentation route for signature generation
router.get("/docs/signature-generation", (req, res) => {
  res.json(getSignatureGenerationDocs());
});

// Add signature validation to ALL routes that modify state or fetch sensitive data
/********** Builder ***********/
router.post("/builder/fetch-to-do", validateSignature, fetchTodo as RequestHandler);
router.post("/builder/add-aggregator-info", validateSignature, addAggregatorInfo as RequestHandler);
router.post("/builder/add-pr-to-to-do", validateSignature, addPR as RequestHandler);
router.post("/builder/add-issue-pr", validateSignature, addIssuePR as RequestHandler);
router.post("/builder/check-to-do", validateSignature, checkToDo as RequestHandler);
router.post("/builder/assign-issue", validateSignature, assignIssue as RequestHandler);
router.post("/builder/update-audit-result", validateSignature, updateAuditResult as RequestHandler);
router.post("/builder/fetch-issue", validateSignature, fetchIssue as RequestHandler);
router.post("/builder/check-issue", validateSignature, checkIssue as RequestHandler);
router.get("/builder/get-source-repo/:nodeType/:uuid", validateSignature, getSourceRepo as RequestHandler);

/********** Summarizer */
router.post("/summarizer/fetch-summarizer-todo", validateSignature, fetchSummarizerRequest as RequestHandler);
router.post("/summarizer/add-pr-to-summarizer-todo", validateSignature, addSummarizerRequest as RequestHandler);
router.post("/summarizer/trigger-fetch-audit-result", validateSignature, triggerFetchAuditResultSummarizer as RequestHandler);
router.post("/summarizer/check-summarizer", validateSignature, checkSummarizerRequest as RequestHandler);

/********** Planner ***********/
router.post("/planner/fetch-planner-todo", validateSignature, fetchPlannerRequest as RequestHandler);
router.post("/planner/add-pr-to-planner-todo", validateSignature, addPlannerRequest as RequestHandler);
router.post("/planner/check-planner", validateSignature, checkPlannerRequest as RequestHandler);
router.post("/planner/trigger-fetch-audit-result", validateSignature, triggerFetchAuditResultPlanner as RequestHandler);

/*********** Prometheus Website ***********/
// Preserve existing bearer token verification where appropriate
router.get("/prometheus/get-assigned-nodes", validateSignature, getAssignedTo as RequestHandler);
router.post("/prometheus/classification", verifyBearerToken, validateSignature, classification as RequestHandler);
router.get("/prometheus/info", validateSignature, info as RequestHandler);

/****************** Supporter **************/
router.post("/supporter/bind-key-to-github", validateSignature, bindRequest as RequestHandler);
router.post("/supporter/fetch-repo-list", validateSignature, fetchRepoList as RequestHandler);
router.post("/supporter/check-request", validateSignature, checkRepoRequest as RequestHandler);

// Public routes remain unchanged
router.get("/hello", (req, res) => {
  res.json({ message: "Hello World!" });
});

export default router;