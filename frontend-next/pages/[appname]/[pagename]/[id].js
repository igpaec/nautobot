import Card from "react-bootstrap/Card"
import CardHeader from "react-bootstrap/CardHeader"
import Head from "next/head"
import Image from "next/image"
import Link from "next/link"
import { nautobot_url } from "pages/_app"
import nautobot_logo from "public/img/nautobot_logo.svg"
import Tab from "react-bootstrap/Tab"
import Table from "react-bootstrap/Table"
import Tabs from "react-bootstrap/Tabs"
import Layout from "components/layout"
import { useRouter } from "next/router"
import useSWR from "swr"

const fetcher = (url) => fetch(url, { credentials: "include" }).then((res) => res.ok ? res.json() : null)
const fetcherHTML = (url) => fetch(url, { credentials: "include" }).then((res) => res.ok ? res.text() : null)

function RenderRow(props) {
    var key = props.identifier;
    var value = props.value;

    if (["id", "url", "display", "slug", "notes_url"].includes(key) ^ !props.advanced) {
        return null;
    }

    // "foo_bar" --> "Foo Bar"
    key = key.split("_").map((x) => (x[0].toUpperCase() + x.slice(1))).join(" ");

    return (
        <tr>
          <td>{key}</td>
          <td>{
            value === null || value === "" ?
              "—" :
              Array.isArray(value) ?
                <ul class="list-unstyled">{value.map((item) =>
                    typeof(item) == "object" ? <li>{item["display"]}</li> : <li>{item}</li>
                )}</ul> :
                typeof(value) == "object" ?
                  value["display"] :
                  typeof(value) == "array" ?
                    value.join(", ") :
                    typeof(value) == "boolean" ?
                      value ? "✅" : "🚫" :
                      value
          }</td>
        </tr>
    );
}

export default function ObjectRetrieve({ api_url }) {

  const router = useRouter()
  const { appname, pagename, id } = router.query
  if (!!appname && !!pagename && !!id && !api_url) {
    api_url = `${nautobot_url}/api/${appname}/${pagename}/${id}/`
  }
  const { data: objectData, error } = useSWR(() => api_url, fetcher)
  const { data: pluginHTML, _ } = useSWR(() => api_url ? api_url + "plugin_full_width_fragment/" : null, fetcherHTML)
  if (error) return <div>Failed to load {api_url}</div>
  if (!objectData) return <></>
  return (
    <div>
      <Head>
        <title>{objectData.display} - Nautobot</title>
        <link rel="icon" href="/static/favicon.ico" />
      </Head>
      <Layout>
        <h1>{objectData.name}</h1>
        <p>
          <small className="text-muted">
            {objectData.created &&
              <>Created {objectData.created} &middot; </>
            }
            <> Updated <span title={objectData.last_updated}>xyz seconds</span> ago</>
          </small>
        </p>
        <div className="pull-right noprint"></div>
        <Tabs defaultActiveKey="site">
          <Tab eventKey="site" title="Main">
            <br />
            <Card>
              <CardHeader>
                <strong>Main</strong>
              </CardHeader>
              <Table hover>
                <tbody>
                  {Object.keys(objectData).map((key) => <RenderRow identifier={key} value={objectData[key]} advanced/>)}
                </tbody>
              </Table>
            </Card>
            <br />
            <div dangerouslySetInnerHTML={{ __html: pluginHTML }} />
            <br />
          </Tab>
          <Tab eventKey="advanced" title="Advanced">
            <br />
            <Card>
              <CardHeader>
                <strong>Advanced</strong>
              </CardHeader>
              <Table hover>
                <tbody>
                  {Object.keys(objectData).map((key) => <RenderRow identifier={key} value={objectData[key]} advanced={false}/>)}
                </tbody>
              </Table>
            </Card>
          </Tab>
          <Tab eventKey="notes" title="Notes" />
          <Tab eventKey="change_log" title="Change Log">
            <br />
            <div dangerouslySetInnerHTML={{ __html: "<p>Your html code here.<p>" }} />
          </Tab>
        </Tabs>
      </Layout>
    </div>
  )
}
