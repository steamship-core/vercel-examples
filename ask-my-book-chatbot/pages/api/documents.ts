// @ts-nocheck
import type { NextApiRequest, NextApiResponse } from 'next'
import { getSteamshipPackage } from '@steamship/steamship-nextjs'


export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<any>
) {

  try {
    // Fetch a stub to the Steamship-hosted backend.
    // Use a different workspace name per-user to provide data isolation.
    const packageHandle = process.env.STEAMSHIP_PACKAGE_HANDLE as string;
    const defaultChatSessionId = process.env.DEFAULT_CHAT_SESSION_ID as string;

    var {dbId} = req.body as string;
    dbId = dbId || process.env.NEXT_PUBLIC_INDEX_NAME as string;

    if (!process.env.STEAMSHIP_API_KEY) {
      return res.json({ error: "Please set the STEAMSHIP_API_KEY env variable." })
    }
    if (!packageHandle) {
      return res.json({ error: "Please set the STEAMSHIP_PACKAGE_HANDLE env variable." })
    }

    const pkg = await getSteamshipPackage({
      workspace: dbId,
      pkg: packageHandle,
      config: {index_name: dbId, default_chat_session_id: defaultChatSessionId} as Map<string, any>
    })


    const resp = await pkg.invoke('documents',undefined, "GET")

    const documents = resp.data
    return res.json({ documents })
  } catch (ex) {
    const awaitedEx = (await ex) as any;

    if (awaitedEx?.response?.data?.status?.statusMessage) {
      return res.json({ error: awaitedEx?.response?.data?.status?.statusMessage })
    }

    console.log(typeof awaitedEx)
    console.log(awaitedEx)

    return res.json({ error: `There was an error generating your profile.` })
  }
}
